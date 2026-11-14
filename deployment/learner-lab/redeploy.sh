#!/usr/bin/env bash
set -euo pipefail
export AWS_PAGER="" AWS_DEFAULT_REGION=us-east-1
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$root"

release=06c2292cdf0aca80f050709b8172fac3595b54cc
source_digest=a0eb70b7e8a9505e912c14fead268e9c0798064e35708243404c250def1abfb5
demo=reading-tracker-recovery
artifacts=$demo-artifacts
ami_parameter=/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64
templates=deployment/learner-lab

aws_lab() { aws --region us-east-1 "$@"; }
inventory() {
  if ! aws_lab "$@"; then
    printf 'Inventory unavailable for %s %s. Review this service in the console.\n' "$1" "$2" >&2
  fi
}
stack_status() {
  aws_lab cloudformation describe-stacks --stack-name "$1" --query 'Stacks[0].StackStatus' --output text
}

case "${1:-}" in
  preflight|prepare|deploy|status) ;;
  *) echo "Usage: bash $0 {preflight|prepare|deploy|status} [expected-account-for-prepare-or-deploy]"; exit 2 ;;
esac

account=$(aws_lab sts get-caller-identity --query Account --output text)
if [[ ! "$account" =~ ^[0-9]{12}$ || "$account" == 214018170594 ]]; then
  echo "Use the replacement Learner Lab account in CloudShell."
  exit 1
fi
printf 'AWS account %s, region us-east-1\n' "$account"

if [[ "$1" == status ]]; then
  aws_lab cloudformation describe-stacks --stack-name "$demo" --query 'Stacks[0].{Status:StackStatus,Outputs:Outputs}' --output table
  exit 0
fi
if [[ "$1" == deploy ]]; then
  if [[ "${2:-}" != "$account" ]]; then
    echo "Pass the account ID shown by preflight."
    exit 1
  fi
  stack=$(stack_status "$demo")
  [[ "$stack" == REVIEW_IN_PROGRESS ]] || { echo "Existing demo stack status: $stack"; exit 1; }
  change_status=$(aws_lab cloudformation describe-change-set --stack-name "$demo" --change-set-name initial --query 'ExecutionStatus' --output text)
  [[ "$change_status" == AVAILABLE ]] || { echo "Change set status: $change_status"; exit 1; }
  aws_lab cloudformation execute-change-set --stack-name "$demo" --change-set-name initial
  if ! aws_lab cloudformation wait stack-create-complete --stack-name "$demo"; then
    aws_lab cloudformation describe-stack-events --stack-name "$demo" --max-items 15 --output table
    exit 1
  fi
  bash "$0" status
  exit 0
fi

aws_lab cloudformation list-stacks --stack-status-filter CREATE_IN_PROGRESS CREATE_COMPLETE REVIEW_IN_PROGRESS UPDATE_COMPLETE ROLLBACK_COMPLETE \
  --query "StackSummaries[?starts_with(StackName, 'reading-tracker-recovery')].[StackName,StackStatus]" --output table
printf '\nCurrent EC2 and load balancers for the budget check\n'
inventory ec2 describe-instances --filters Name=instance-state-name,Values=pending,running,stopping,stopped \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType,Tags[?Key==`Name`]|[0].Value]' --output table
inventory elbv2 describe-load-balancers --query 'LoadBalancers[].[LoadBalancerName,State.Code,Type]' --output table
inventory dynamodb list-tables --output table
inventory ec2 describe-nat-gateways --filter Name=state,Values=pending,available \
  --query 'NatGateways[].[NatGatewayId,State]' --output table
inventory rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,DBInstanceClass]' --output table
profile=$(aws_lab iam get-instance-profile --instance-profile-name LabInstanceProfile --query 'InstanceProfile.Roles[0].RoleName' --output text)
[[ "$profile" == LabRole ]] || { echo "Expected the course LabInstanceProfile / LabRole."; exit 1; }
image=$(aws_lab ssm get-parameter --name "$ami_parameter" --query Parameter.Value --output text)
root_device=$(aws_lab ec2 describe-images --image-ids "$image" --query 'Images[0].RootDeviceName' --output text)
root_gib=$(aws_lab ec2 describe-images --image-ids "$image" --query 'Images[0].BlockDeviceMappings[?DeviceName==`/dev/xvda`]|[0].Ebs.VolumeSize' --output text)
[[ "$root_device" == /dev/xvda && "$root_gib" =~ ^[0-9]+$ && "$root_gib" -le 8 ]] || { echo "Check the AL2023 AMI root disk before continuing."; exit 1; }

for template in artifacts demo; do
  aws_lab cloudformation validate-template --template-body "file://$templates/$template.yaml" --query Description --output text
done
s3_prefix=$(aws_lab ec2 describe-prefix-lists --filters Name=prefix-list-name,Values=com.amazonaws.us-east-1.s3 --query 'PrefixLists[0].PrefixListId' --output text)
dynamo_prefix=$(aws_lab ec2 describe-prefix-lists --filters Name=prefix-list-name,Values=com.amazonaws.us-east-1.dynamodb --query 'PrefixLists[0].PrefixListId' --output text)
[[ "$s3_prefix" =~ ^pl-[a-f0-9]+$ && "$dynamo_prefix" =~ ^pl-[a-f0-9]+$ ]] || { echo "Regional gateway prefix lists are unavailable."; exit 1; }
if [[ "$1" == preflight ]]; then
  echo "Read-only preflight passed. Resource creation permissions will be tested when CloudFormation provisions the stack."
  exit 0
fi
if [[ "${2:-}" != "$account" ]]; then
  echo "Pass the account ID shown by preflight."
  exit 1
fi

if existing=$(aws_lab cloudformation describe-change-set --stack-name "$demo" --change-set-name initial --query ExecutionStatus --output text 2>&1); then
  echo "Change set already exists: $existing. Inspect it in the console before continuing."
  exit 1
elif [[ "$existing" != *"does not exist"* ]]; then
  printf '%s\n' "$existing" >&2
  exit 1
fi

python3 -m pip --version
work=$(mktemp -d)
trap 'rm -r -- "$work"' EXIT
mkdir "$work/wheels"
cp app/reading_tracker.py "$work/app.py"
printf '%s  %s\n' "$source_digest" "$work/app.py" | sha256sum --check
sed '/^#/d; s/\r$//' deployment/runtime-requirements.lock > "$work/requirements.lock"
printf '%s\n' "$release" > "$work/RELEASE"
python3 -m pip download --disable-pip-version-check --only-binary=:all: --no-deps \
  --platform manylinux_2_34_x86_64 --platform manylinux2014_x86_64 \
  --python-version 3.11 --implementation cp --abi cp311 \
  --requirement "$work/requirements.lock" --dest "$work/wheels"
bundle=$(mktemp)
trap 'rm -r -- "$work"; rm -f -- "$bundle"' EXIT
tar --sort=name --mtime='UTC 2026-11-07' --owner=0 --group=0 --numeric-owner -C "$work" \
  -czf "$bundle" app.py requirements.lock RELEASE wheels
digest=$(sha256sum "$bundle" | cut -d ' ' -f1)

if inventory=$(stack_status "$artifacts" 2>"$work/stack-error"); then
  [[ "$inventory" == CREATE_COMPLETE ]] || { echo "Artifact stack status: $inventory"; exit 1; }
else
  if ! grep -q 'does not exist' "$work/stack-error"; then
    cat "$work/stack-error" >&2
    exit 1
  fi
  aws_lab cloudformation create-stack --stack-name "$artifacts" --template-body "file://$templates/artifacts.yaml"
  aws_lab cloudformation wait stack-create-complete --stack-name "$artifacts"
fi
bucket=$(aws_lab cloudformation describe-stacks --stack-name "$artifacts" --query 'Stacks[0].Outputs[?OutputKey==`Bucket`].OutputValue|[0]' --output text)
[[ "$bucket" =~ ^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$ ]] || { echo "Artifact bucket output is missing."; exit 1; }
aws_lab s3 cp "$bundle" "s3://$bucket/releases/$digest.tar.gz" --sse AES256 --only-show-errors
echo "Private bootstrap archive: s3://$bucket/releases/$digest.tar.gz"

aws_lab cloudformation create-change-set --stack-name "$demo" --change-set-name initial --change-set-type CREATE \
  --template-body "file://$templates/demo.yaml" --parameters \
  "ParameterKey=ArtifactBucket,ParameterValue=$bucket" "ParameterKey=ArtifactDigest,ParameterValue=$digest" \
  "ParameterKey=S3Prefix,ParameterValue=$s3_prefix" "ParameterKey=DynamoPrefix,ParameterValue=$dynamo_prefix"
if ! aws_lab cloudformation wait change-set-create-complete --stack-name "$demo" --change-set-name initial; then
  aws_lab cloudformation describe-change-set --stack-name "$demo" --change-set-name initial --query StatusReason --output text
  exit 1
fi
aws_lab cloudformation describe-change-set --stack-name "$demo" --change-set-name initial \
  --query 'Changes[].ResourceChange.[Action,LogicalResourceId,ResourceType]' --output table
echo "Review the change set. Run deploy only when the group is ready to test and record."
