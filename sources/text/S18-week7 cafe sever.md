# week7 cafe sever.txt

Course: INFS3701. Searchable text; original diagrams and layout remain authoritative.

Classroom demonstration only. Do not submit the Notes/cafe worked example as the group service. Do not execute automatically.

```text
{
 "AWSTemplateFormatVersion": "2010-09-09",
 "Description": "INFS3701 Campus Cafe - Week 7 add-on: launches the cafe servers into the network you built: a web server in each public subnet (public IP) and an app server in each private app subnet (no public IP). Each web server forwards to the app server in its own zone. Orders stay on each app server until the Week 8 database.",
 "Metadata": {
  "AWS::CloudFormation::Interface": {
   "ParameterGroups": [
    {
     "Label": {
      "default": "Your network (Week 7)"
     },
     "Parameters": [
      "PublicSubnetA",
      "PublicSubnetB",
      "AppSubnetA",
      "AppSubnetB",
      "WebSecurityGroup",
      "AppSecurityGroup"
     ]
    },
    {
     "Label": {
      "default": "Servers"
     },
     "Parameters": [
      "InstanceType",
      "InstanceProfile",
      "LatestAmiId"
     ]
    }
   ],
   "ParameterLabels": {
    "LatestAmiId": {
     "default": "Amazon Linux 2023 image"
    },
    "InstanceType": {
     "default": "Instance type"
    },
    "InstanceProfile": {
     "default": "Instance profile"
    },
    "PublicSubnetA": {
     "default": "Public subnet A"
    },
    "PublicSubnetB": {
     "default": "Public subnet B"
    },
    "AppSubnetA": {
     "default": "Private app subnet A"
    },
    "AppSubnetB": {
     "default": "Private app subnet B"
    },
    "WebSecurityGroup": {
     "default": "web-sg"
    },
    "AppSecurityGroup": {
     "default": "app-sg"
    }
   }
  }
 },
 "Parameters": {
  "PublicSubnetA": {
   "Type": "AWS::EC2::Subnet::Id",
   "Description": "Public subnet in zone A (e.g. 10.0.1.0/24) for web server A"
  },
  "PublicSubnetB": {
   "Type": "AWS::EC2::Subnet::Id",
   "Description": "Public subnet in zone B (e.g. 10.0.2.0/24) for web server B"
  },
  "AppSubnetA": {
   "Type": "AWS::EC2::Subnet::Id",
   "Description": "Private app subnet in zone A (e.g. 10.0.11.0/24) for app server A"
  },
  "AppSubnetB": {
   "Type": "AWS::EC2::Subnet::Id",
   "Description": "Private app subnet in zone B (e.g. 10.0.12.0/24) for app server B"
  },
  "WebSecurityGroup": {
   "Type": "AWS::EC2::SecurityGroup::Id",
   "Description": "web-sg: web traffic from anywhere"
  },
  "AppSecurityGroup": {
   "Type": "AWS::EC2::SecurityGroup::Id",
   "Description": "app-sg: 8080 only from web-sg"
  },
  "InstanceType": {
   "Type": "String",
   "Default": "t3.micro",
   "AllowedValues": [
    "t3.micro",
    "t3.small",
    "t2.micro"
   ],
   "Description": "Instance type for every cafe server."
  },
  "InstanceProfile": {
   "Type": "String",
   "Default": "LabInstanceProfile",
   "Description": "Instance profile for the servers. In the Learner Lab use LabInstanceProfile."
  },
  "LatestAmiId": {
   "Type": "AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>",
   "Default": "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64",
   "Description": "Amazon Linux 2023 (latest), looked up automatically. Leave as it is."
  }
 },
 "Mappings": {
  "CafeApp": {
   "Bundle": {
    "Part1": "{Wp48S^xk6X(HY>0stWa8~^|S5YJf5;Gh33#9aU}m`MhmSr8w&AI5Ev)18O;?I`tYYm7_(i>6^_zMhFJwMuEiMuUy~Jr@2mro-}YH=)1Y1wTMCt@kj|u@MR3(3`2vZY%CxTessP%(r*P?5E7?b5~|kx8t@tx&9mm!od5%EF#`#@{G)jWB4Eq+wxrG>;v$$@BIp_{j!CL#e(1GktE<4QqedQ;en#wp0tW8G!u}z@!IldL`!&E>+N8>_FAXthE1T)6T@jS1+xV0)NWSA0gzWPX$kh(h_X8oNK~RPTWE16)>3h#yH4rwH_Y^R15Y3)hbVtGMpG1gyXQ8W6J-a6NY{x(eAeCOt&hzi+XHcZU{m7Kf>m8|Qv<3iUrjUTQ`#;yK&h!G-;a}sr5}x8K`A0&Xl^r1C=L}n8EfkjEx&u!CBto!wpb_9Bt|pU*_(nwhtT+dSmRg!4|STNCJX<gHK~9G&B-cPNtR+fZyzDGSNq##!J>mc>8U8VRn+{@A|-1veieUPA)YAXn~%D4lEdq(BkZsdiKy=>!msVb6Oqi<<JPidO}<Y71}=?C^>n?@kbXP1iadR;eXH)1H|6Kq`8&In4QYig#u_9Ibz`mxmTZeIbCuAGvn4)wCB<Ba1fD&4K)Qj|=BohQGtceudqYI|wNg&G^mu$ZNP^;<=Fw0vAcQIm;{Vn`+9$zkj2;Ja=|xfZp4AJMZ<!C2@_SaZG6CT&uiVStVNb_xi@ib*J`(Kt%XeSs`X~!=1`JITb^e#%xuHoSUH(LjLKoe7YC!aQy3{xV*wC>UlBiTrVq4d02`Mdx?@J@AU^1pWo&}_yf)m~{PjsB^sZrOoa2^RAf*dc`#pJm106q1$^{dnHm;-}yy?fp4&V3iRx0{49OflKMvQaus#19<Y>5^zxIJezZMp?s|4f`*+x~yF&WWl;5Rs5&{)wlR}H@fFO%YuhdwTR2>L+KY5NhEUnX*?wiOzf+{8>_s+FU1C3sC+CkuE}z~R4a>&f7(kpnQcVE)3cAk)g<H(?l|PRiB>7zmj{QAqQEz<EKLlpvebHyi2G&tMI|=zQE{f~5ugQrXV^L}zi7I;=g*hKgW>^~C$KaZGF`z7m^#I`b(rJ}!P|ZjPoI5{_s4T8CaxI2<&rvPC!H_n<nQM6?GD;q-5mR}+jb35JFpr=Hjkuai|451_1fv2Ez#20Q7-lUcTKUrP)STmP${68E1$1{W#_W_Jvo1W%Y9mbjn`LOg07lxgFNkr##y*2`Eg_LctARPOp?#|3x)to3lKY?g=%QLO_--Yuj{}Bq1ET`EG0-^Yo?2tVJqF*@Dj2nQ>|<X*oO=|qMtl!*{9tJnT?ExF<B{ft4R<4KJOaIkO}2s#lknCGa<mGxNoLjZ2CN0-ZTrhkAd?1%?9`h^zKP3iR@}VN6I=oAw+$Mpz<zDN#MZWMJ?(EqFfMnJjmDoU5!MJb>9o%%}RnRmtCoo!r1R4eXQ5q1O~_p);qXmz7zv~4(M*gLX_jW<Db87kJL@Sg=i{8IQDDpt8QmzW$UVLv|+n5PB)M*JHBG?6$}NcAQ{t!E4t`GT#If_2;w3Ev5v&m)NOxBkU1fF0o-qF^f<l5Nz}`M_Swv<&-_p~%Hvc~J#XzD*;-yi-JNuSCs)D70Z7R3w%dt*R>E*!Ktz_+CdS08okN6>yJ}FP&o!2Sl5kh24HU<CkjvvmakM9%PJuO3oFai84OPXQBish%JidcxJHfRq_Qa=!moF4X0=B8@o|(Uzy%kjSOaLwuwdv~|5K{7$%$YSgJ*t25r}x$X6)8lFyLjx*#Y5~ix|gL+&&xwWi!;N>t=ifviGo)XW$>u8%grK(-RgZ#A0?B|OoMFCHiUpyNq3<c0`3?-NI$Lxy%q6<5Zb)3Vto_lNZ%{^Xv3%AiH&Euvk6Dhz9Lp}U14Sut2^J$38u?sq396;=SqGt8r5Qyw%`~pl^7Fqb2xWAFfmFF%-YXkKCTugG%@?|D&~Qe?PDq7xJ<-vtcL0`{lBfilHhW*#tNzs9xw%L^6v;KvD6sKdC+sKV%ci?7SH54fysg30i2)$rmgV}-p_?W?wVjjS0#*MMJom?LFGo-I&@~eM-vpS<q&@I!rq`xpECCQYOoDRV8BoIx78_sAkllv(HczbIw)U$23x1HL?r+?A_@BW&{=|_g=iLEPsLyicrCMeveOJS$!BOb#H~L^5ZYUxn~%xlV`KSuw`WKbMajoIPCaj@Q|#DFJ6j>0H7?7NAtd+%H*{J(WC!4+rrBkt$`PpIcL?|NJCL+Tb=I^!7gim#Alg7%=_ZICRR}WGmq2DqC0(gm{_D^(S#QkhM;#C2YiW@?4$gX*LNyz=VESz&9>{`k3+hqK2aGUZcop;hSHv+kAS<1qZ7}zM!`|o`nC1jLA;jbI6jtF~h_EP#I9z`u{)f5XjcYYu=wiD9g$;^*(7>r^Oq$}>jr&=Q0IUE`7ZL59AR}$zV<UzB$iRCxD@k>erd71?VWn{R(BN#ACAL+5-$cU4cQvSFE8~-X9yM5g5_&<**1~Sfv7kMG&9p09O56&&?W{<s>pAn6h?4ULz}jIm)BVTy6AlBuH{LrgUdqisr+weBCK%{9w~Ky#U38w*^z%H?5lb?m6<0eK@yP@Z$m%ZI%vKcC<oNx9_)WQ0T6SA%m_icMJ2%38Xju;bpJa8C;w@m%+3ijSAyjl+M1(bn)aI8YV_T%LDW>eG?fQ<}5uuUawYnxAiI~UrHRio((o}BkUM!hOCdAgjJ3fd&zcwjME&y6?Tf#IYhuzK3R6LJYo0iIN2qQx#in6R$w~>yhD*TNSy(cJ>S2yYb)P&v&8=$dmUpe8QV4;qLjt-mx0RgwRmMiu^sXSJJ`2S@dpsddvW~Qv??`XU&|EP?K%;smA8O-gQkYgeSK6xieEn-1b1*WLKfiTfS-Gs{JAi}qGdofk^2n!KkX5b0zG#qX^b#m2^WboN}{eWZSNttv5>Y;7D;P^l0Zvv0WaNuR2(x2pXpT=TN-#Ic39L`enZQL3uJy`yKN?nqS7W}$6Y8_?kR!gO+qCk`|7ER3<t$08zI{L@1`_519p(bZT5ZFSBF_Q)KTVml1*^P$?Y7v?PJ>|t5fJA00lmIau`LAw0XyGqVQ7_JhXM0jLtb|#iENAAc!9(wM9_;q9Y*#G(?GXs%5<lrX4IjrvZ~fVd-9nfwyEibzk2xIOzat+0gVY0o6AL>A=nM~U#IW2F<w6@5s0~Mi>SLVaAe3d_QJ`g;9;FieglzHH!PESac;*g45@PB~J|trdGib?nBbn?aI;h{>Pg%yjQVuOlsCl~0tYk|<cgvswp8A89+TbA(LF2-;4KRluJ{h?cSYq0XJVh88Zbq0h?sS8-oS+Yh<}#67r!*Kzcqt^=1%Fk--%}$mMt=yw!SGIkv3R=%I~z*0xjAmC47ntW?^^@S9bSFxGbi*3tDh*4B!!^M1<ZDwFVynv_3eoT9?+E&r(z@X*)RT{cmKt&Af&Zc0)$MEvndIz%Q;VnNmQ1QxITI3FLOpR?{w~9soHGJ+ft&!b@q_^Z`ACnAKnW$gCfj669!OOpxRl2FxuUb9=?m>nV}|TuUsZ$6or0?Xs1zVU>yzWQJDFJ>XTy_K5t?1I(nNPI#o(>Yg00Mb0ALMCTw;YS<7?zG3c$=4CM^ttZ;a55dtSD1ed_K4Ykp!wz^M@?JXZO#o70$?|x5$RgGDeT0ym+^3=@#Nt*>ev^oZ*wR0i`dfEu#W2#=dNZCU!ujtKTi-CIx>pN14+dO49033+-nUj<DPdk&Y9Tx`2eP1%7)xKhM2N+`H4m*>M8qCl{hMgWR;WUoEX#|NTnw`bM<s8+<<2lwrhxN*suwHS>0(_MZ;|~pV&5(U&eTNEi>h3dKX56wWH?eP}%Z`-z+IGYmOPAse6#C;-?3&!FRnL5SQpmAim615Hb<@xt(o!ZrfhGg@k3V((JO{D?cQMykg83xCB*m55Pb_QQO4qGvOKMppQ~%3Kxpy47Wjz^2j`GTYKvhQ5M<J3L#^huV-ChmP#PjZa;Yvu@g)V0~!!abuD9nk6`PnZ^oI4ljM;sq5WaC1@",
    "Part2": "Z#J&Kzl5Jjd82;{wxL5{$>?%g?<$IbccX+$IIcB~$xxX+iKfzA7TWh*B-W9`e(mfpy7b&I`)_gRN?+WZ`_{4WeC?lRl-!_y-$w+Ugwe^bt)nUGUe-8&nN#&n$bT<e$&B(t?dXiXN@s}G_ZQYG#hhH^e2<d0-R5O-B0~}$!*sh%Q=NpQG!~NbVnnR((U7fA?}`p^!TK%O|A#!MS|9w?(ZNKl6956*#BZti!5dS0h9H;SbIuySVgcaD7j`PQ-ThD^z?$~sBt`Us`t}HVvZv`l)IXe45n6MOOq)^bJLC7&_z}`X&V6g`-k&HjuJUzYQmPzq;Y`gtn+LA~M~l6s8@T;JLhJD?)gK3Xg<Dfnclq)P0vBLMpuV$n0?zjj(5teZhgHufTi#32LD`zlhl7QBjVOo?VqMy|AFIGo6Bdg-vBF+n7)afhZiJW*Xa|?SFzNvy+ABbx+bnkA@*X+5HW%Pq4j}bklFSG``4qMl@5_pD+t)B_Jlwodzr#Ss<+JdbLi8TSP~O=g>}nIRE*NKZnrjH&ecKq?79-%F#!MpW8GQ|M75<g(!}w3KJ?w8z&O!M{y=u$b8~V$OCzkiQG;?c{tD%<az{1J?pOM6)Pm;r}KpJV;1{_l3_k4gYDHhmORZ7rv6Q`?y9@(lkB-+T~^JPd%VjCy2Y|_*o98>YNyZS0B-6ZP8_h6ot(9Um8VFbS==2RSBF>m!@cff2+Ipq^XOhwGRM4oo9576$g3rHKK2Nn8X7~fcQMM3|oVsZ9!pXso%JzOJdoSEWD6#QE2jdL)3MuObyr5HAa2{{wR6`VK|fIX0d#Uo4~1U$f2{`x~W8JRNbT%LVc-O`xCdNYc1)`44Y{s7R&P1a#3$LgyxC79?oS_@>^{0XH?7Uqc)*OG2b<CvM#LbL-5A{7_l?L(|SSy}SWYeLFYs}>W+G$!8;n))Vptvn%S5U6=VgHe=?H?jGVYxyy*om%u@{JDAB95}V~f1Y5GYRW4|wUiz0IY4Exn&as@)mHpe^<PAJO$EfOzAD2qlR}S`4Q68et<G~}Tpy$cjzImsDUxi51Mua=jbV}vCK6>B-E!y2Tb*Oe4pBulLzYh+A(dY5olHuk$Welv)bbZ8^ok^6mzCuOkU*stQDAv|j0d-cv~fq2;ln9tq3umZ=2-PR0m}{2NTgB;?6B-3w}CzYaAXgqUr#`Eo!+(H@%ld90EE|pBh@Sd6snwA@^ex^C*I{~nIcP?H5Ri*n2(JliNlJF3jp_r?hFa}IJ5WhkNHM^Vo2;+I_@Tk$Y@)1`@FsZ{iS;)+V6>yh=wOT<;z@v&g14b(l_r#a3Uv6g4!u|Nd~HL8i+O=F(G}Sx<|hLv(Srhby@THv!dC7<m}O0JE&ZiF}DT>oc0-GA(6%j0o0ZL7YyDtQ%_m#sGV|pFcA+eN%X(~2U#(&+%0?tr**mus@~s3F|#{6CKuI<v+UnHiY|g+0cC~hI>P(%wDp$;P<#Gv<NOg?B9<+QA{(~RP@I&5IFw4rl=S)^$M5+cg00Zq&?g1T(vDmP%a+wpJgyR+Nk`jQ?oVQ!cmsO}Qqgmt%C-#>$|da488&ubv}{5STzA(U+@F3I2}s3fxJ;+nii=9_^9W-x0oYU)ecrwqF$J7)#sz8JyAUw)y2rcHzxC_hXlPd|xl#e{3V?@>PTrf<s>)3@#$#9K&h}oS8i^RaLPh61%5*{?RUxzZMxf!T{XA}Db#hhgb+n*jTdKTG`2B*ne?|iM$tnL5{vg-o>VDv5se;V%qsaB;5+U{!D5bFCyQL@*qLu4tiV{d6@+RMtjWRzI1s*#*+MT`wnshU`a8(bRc3cmi3<d_UWvoC{H6jAxQHQw^iL)){>OL^S1UGDK_8CKeSd~=p_k9JsKo+&q4w6K#)Nk`MF>$hy#l4R(^9#D{bts*1eT<H=hQ=4)E53jsBzt2T5U=}In+IKt?F;mSyx#sXk9m|N)L5uXxDIQ-ULjxzZ}SgLM_J5Zu1NvgWpQ}7F9G4qE)<*w!W|cr1?j^N+h`VD7IdP1wrx|WubXzbz_(50@@_{2)93W(x^C~cgIU!FfMP8#?738p@@a)1rl>yrh8R$bDLkuqh=;NVL`eScGI?k}+dVVM{4|GzM(qr8y$jX1U-w3<c(V!`RhV~Ct#Y*5pS?aP3RRppGFAO=CP2HH!iGugVA#74QlN<Sga%ivaS^FKty_vT)kyMSOF7^2tv?7FC}<N_656}ez3vvI<Wq2uHl2W}{#BCLA4R&7LD00wSnX&h9cGdJhYT1n3$$qR7T{7u7EC_FUpNlCb-h=E<W>G}uXX=b!3SvpOzMjmd(|I4is%W6libWfcwTQmkPP3ERh!GTy8ZgknS5V*($S*i$zDBQO_mZPGv#++>0+RnA}Ciw@jwST?dQ5rmL9a`o*LHMf_7?Li&`{zWawr7H%(vrAylLNAVM4{)NFiCYe#uH;}{-=$_MQKn_~o1nfn$>G$31~OJv$)wZ!+EYo2Q`tD>t09#IKp+eVbiEk#q_7$EX&^_ZPmlsXBFK5DMjzOga;%$acI!tLEa)0kT&8*jS<=tQBlG6BxF%2@EZg$-5j>3#t0$Y0jIvH;eh>g2r%t~H11a}QO&O5I?D=AW&>Lg4jH34I1dCQk4^RSj7J@^3EC&1Fi+mBXQn+~31w^~jcg8v?@Jvy%;_kB_|E6FaVXTtuIHKrXl!?6QV?MBJ4R$ff{~AUV^rj`(^bG*VKye@+rq*14_}A@l2?Z6lXIJkg-*VIpRyb9U>P3G8GtMY$d$X?U<R#B9@flHXikMuUJIlGe~xiXKSx292?nW_3pU45O-BizibPORDy8#RvwDQ+i*B7GdO-6QZz7&uBgJN|P$f-t&<VMt}OO@lS^FMNmenOnZV9oKIgH^SDjGERLXTZHDGO(h`QUhnWRjeqsFgV&#y8-<y}pD$4w=QNHMrKz~+1dm&*_IvLXRF0@cWqH|!Hdm=eYM!fd=&HiO2wA{|$9&G{x#NgJjU`Wt~Mfws&YQ{*KvS-`v#oe9@r6GLZNS;|L=ktw;h*Ypx+>i4%Rp5IpXDJI}UMxsCwi)5N_Uev#Sr*C&yeO8W_W#wqP(W!^oXk?45W_rLohiBXq-dCS-wP|IPKUWUq~`YT;^YDV=xud45}gx~>&p}{W5&6*sE@fG?s1L4ebs<Lu-Pq%6DlTQxVlF(9@Yt?V!eO~fxLZN`kanG2Q{-;E!JCDVbsbx`sr`~anghKc1e3}ai5OMp!hI?!YQ|>BbaQg%^6h`(_4y+bzzoiKj@14vW7RCp11VWWM-k%wu3FQCqDA04D1`l^`KzwD@r149uLz1bM2hIp<~<Bv|eLZXCbFhEWvgX6}Epvv~SB9D1zj}1KIyIhzQ}ua=W1V-bpU3&5urg(N=y}Y2ChnF3zfv1TFnI5(fC}ZNd?B^Df%NnQ-D4-%aDijRF`?%5KCkQpyXW%myjk&oewYa;1YKG5ZK@r^c6nqbl=q0Mt14dPaR1yWGIQc+iOp?8;Lu@w`xP7|Q41z(t;>oblIuS=6;@0+4v8K>Z=f`4m=F88xBKc$NvGakS{KalZyoTijM3H;_W&DZA;mSj9>M`ZEcTNUws?Pb+EG&p{g?pF6Kky!<81OlHXb4<+g5s)E)kbCnmf<{#G9hUAfOU5MoZ#NRaf-1!RE^ur9_5Bmm?ezb4x)1Wm~$Cj;0L6m^%Wq<X#r8HelJ2l#hwPqVitpgRktVYCgUCT4)4xuANc$NdgS1jL<?oJyuL_pPjGe!0Md)7`8-C;x~cgpV4sBV}U9sl%!K4ddP^ITCB<AlNl`$LjXT&yLQ99Fb74{Bm}+yTOw=R?Vk%VvXcF-vW{FA?VqQ+T`m4xuj%$&V}ku%Ui`b;2DR6`E2z6F@_+^sZn_VD7u3+8;^ytsG#?qn7!^EK}Od(S0mCj}Fjj`@+~d_@_QWC~u;t4>j;SP;@zbO0GJ(njI7?3eBT_yHZ_Ec?#r+Z15<x{wlYMZE60}&ksKmJ4ru~2SUi^{EC}?1B4i5yr7>H1|67a`J2-1*uf)rY5|sBm#-k;OQ~a&*|+c^caZ9DsinU=i<>mB",
    "Part3": "Ps2RH71ywqQ&`<(k)G`m0pA5iezOSQZlQ(N_IssV{|6q)k=p&i7T;;^t1~lmer~DCyOegLHF(2*HuZZ&!$;)F3ihOhIJy&QdN^$?^llnHo;Q;Z@0Bw(@?lj|-_gnXQX8Nxi#}xe^uJ5cDTf#y*O{T6gsl^%D&WIP>j{ewKao`XA5yvn&Tsn~doMJ^WCw;tv){S*VgqaoT@0$B8=hFu3!_jUvKdUl#<-=?72MJ;QEsUagvr2wKx6EbBtHs!%4>aMQn;)wZ81ux2H&hujc<HkUGpEa2e%0_{z|)b3E)-R*Y0Bsi#<#WN9~F5iHG#JcT=!pUVe0fO^ipcLdnk4jqNC@F+Rj<&7+}Xuap92QpU7S^cK!nU}v*W{-2WRKC$X=XW^<Df-B-9JTKQ)69pN2_Ky39X3658qIe)L-z`megU<2A2<|f~w-jTCM07f*YRJh0-y=7-uPXO0y{_Rn%_=q+2u}X&R;Xp(UJrKRE{-f1v9s+x#|$mB?l?i&k`u|E7TxKf6TCu#S-Ky1NCHU~msft%GS<T2oM}ArUu4Yfxi|ofd0NE$O3{MZx)Bie1M006T?-Tbp$$S3j_K>u(t!Q|r4Ey<6CwBX?C+?B2f1Yz!BGIt1D=@L9gw&Vc8UpDSi#CD`?c>h^%KIE&tXA<ov~a1po?e~LVDCu;{#<SN_tSj=5%S^;GN@NPpFZ3?_J2W(bIBedXH5PoX|sdkDeyK;-62Ix6|)pJ*69bV6E|-v|JA-Fm-1j-D@6HpKU&<2;B7>bCs{+d|XhXJo?4YyA^X--nxKjuEJ?YS+)4IBKAS|&@4H_5#>JlG=<T^%f)Ciz$1NVv4b+UbB)Qv^W+c=7|wG8tae>D@EOPTE+^tfS5xgKD4Jve#ZylYZ049*^k?X~4=i<H@W8Ppfkp}BU;Zsa+m<~6w&wef$Id4y`AG%cMUA{1Se`Mzl?h@bI-CL91>uzddgP{5T__C_w4tH~V(!wSQU8CP2q0+V#Xok)Q<e&M=k50bo!v<!6vJQuS{L5k8LNjyW-9l~Dd<L`PDaC}K5^y2p6u*4ihsla9NROM*ScS+Q@g6FHkooM>3(UaHsPd&A%#!_B+%xxOHv8l{z}az^cI%2iI2nGLVo#FE!$Pu7qGX&SC>~qa;krebKTO*^(bpBy}$_sFYo!or#t$fp7N{K@35M`5UC|sslM_kBbD9V`vG;UD&{gT0C%oUAlH7a!wCh<l=VR==lNf^FXh6f8iI@H|JNOzvW;RC?U)i5aEn-oQ{l*#0?P6U>fyo#LGLwL9dNDk>PgdrT_OPmU!+L__zW)bW#}g%yRO*h-!tz$5-PAM|0#TM+j$s_E418VGU9%?C5N3asK$0^DUNiX`Lg~<L5JWBN+2{xlIbpQeLuR*`R@B9Lw$PxSZi}|qb<alJk;)39v&9bUpyrW6EjJ<AR<>q0F!kiABebjMI7?^`O2zOAn<Wq(#`J&$VPRC(6wLiu&ejYo`&I5A9fT%UUGvikD&WU(f9_=YT9IAbSs#_9SMW<EGd@}0vU^ox!#Oe2Dphk+LF9_hOE}>`cfYFDqGFS61Y&pEw=%lsMq_b`nEq6hL$_cCq09W(h{1wO-W~33t?u}3iG}Mq&&Q_u{?puJETttE;maP+5W9=B<nFM-I~j&-%YnR!z`-D85u3|j=dAeT<VX?&fphRST?!-*SAOq9PbDPeKu0Lrx0_}Y%1+d+K&^UO%#1kI&ZkDd8%LWt5<sNVuTj|*CaP*P&|+Z+OGKXBrw^Cb2guFJAVLV4L#=prxYMM{=x1Yit3o*B85C=c1>aT{0bpF2Hl6`2-iw=u2tA@?K}`x08?C+nS0o-eUhMX2?&gwd@h;7&+lw?`GS=$FJu7kEE_q=Ql>0}WKip%TD==W5qhLbXt~3c-?gIk2PwBho@c;F=b8};MH>Yb;TzZ`rFCJP;M-wdgP*~8o@l~-+?CN3*xV;cZNSYirBu9-VPn9f+QMACq|LRhBixsb{=U2}R3RmES%BEv81l6^px58g0CyuV5aQ9ONs$8S#7sQz&&}+4(AMJTry9st2zCufdF$o>1C4B7P&x<F4EDX3KV#D7wd3-^A+D>YRlZ|Ao$&?@zWI1WM!!Cu?|L}@FQ81J&SI@2)5&Ff4P-hRh%PiB>Urg~+sy0e$WB8(HzXo4vAo5yIJDGrxHV7C6*itXpnWN0zo{=$Cgmi)y7ONP$gkn3<sJ|};XX6XRPiVFP$$mh_rXcbN^}4pwL}b5q}5UNh3&;PY!t62<hI+8_a6g;2qH!yf{g|YksZwImV;FdJ{uH)HWURSikA+7$JlNZl-rDpxdn^!5Y;pN5DphM|3aG0C#DC&v^0X&A|f4Yy$YP}C4+#&|0LuRv>JPXv|2mNr%VS(cW3&k7Y2VOsh*-(;GoK-_EXfUG3a^yev$$Y7wD>JWg<|9;&^o=o}4>L9pDwf`14`tWe1_zycH?Ieu=(`hFj0kJRK&lk1W+0L{&&p>ITBs>xrMvgdqhdi7+UmA)G8VyBe-$w0lQMu9T04fsTcAS$EY>K;?yquqf(zwUpy<ogQ=7l*6C}=d9p<F{0~`lh-q2`yeX;YtaN3pjLm2`CgO@Av}mE=~IFh_^n7kr6x1s^CM%euI|Trh-(o^4FDM!a7CF|>C?At`Jn&+v2O-lbx2rm3Zp^ID4Ss`5W9k31Hdh`HBfF!ob3lKneOc2GpG`uO<e}tvT9+gHQIn7%1PufcZT4mk()#8i~(-tMMSi4KC9IskGG<{|Kzr*RA6k|=DU+Ovq4U!e?Me~)i_guYu0K>Cm$D!L3&po$iM@}ZJ(Fj#0$L|dUx%@RikN3^acJq{uqo8@w|=+l9#&9%XeWSNY0hSLYs5_RpOPzIbZtD6L1IDZ2mBL`+!beG=et`zwxCHSyJ*h^L2<~*a87qxo&u73lwRfg9Q{wwwK_e)Cm)$l{S0SGd|%qJ==m<w*6QDw6DXR(A`(F#S^~KTrP_?`+en8p;Esxk)3`s8lcm(w#w6t1<-=%Bu(M7b<o)5_=bhgK|$V_hc35c<)2rCQ$FohQ}m0ha*QAkUiGiejfhm=bW136K$}Op2W3p#XRqA1=G+y+_|6hqCl5u0CGBS>2#1$B3J<Pqq+k_m=x{ey8frB&w%7v(^a#yHEByMr=1@u^_4M#`u|<ur_`{ppy*~l-l?*T9)DNxZDK;(34r`19_}vhjiYfULuH##+vBYD%$h5xpayeRbgj~ZifkYj+;t&L1!7q@K5m^+Mb%0dKjFF>^w<`uxI)p^W_)l(7Gnum5H2jbB*h#0kNGRo%f`^j)aPx_?K?Tgi$Xh9S3Utfazz@s(wPI)ISqJ0%4sx6Zn@;|kS@q~*4<K{f;5&zC_tl9;e|%QYFwp!MaIq8}YIr5ar9kv4*JmDg^9C(Tv?|v(WoUzxwU(#x`_qj?oNrv!36Kl+`30#S1>I&=CO&N1TEI*<fo{#2Cq0*%?Zq*@SkYV8whD$Xf3Hb0QJqzZ4}-rR-9q2o1;-BxD}umLC=B#`d+G(;z?Px@PxaJd{fGIzMFcxsNYmLQQ(Cf%7FNh77W8d(LmU?Ov>Ad`KsLS1LCnHNp!_ZjQUa+A&MXDaI>kTP^e0Si_C*5xD%w$-t?0tnAixAB)!<6QQ(|er`E!8wP3B$y{>`b5%<6PHk`!`6W~Y#PfOu}F{;@J-M`!myA3Ty!9Z`djYUv7QrFmE7Q^rdqe@A{^R(+cY-R;|zG<&SBeU+EnI}<!%h5(cQT*V6bIBX!|Riww+hfP=}cLOiUJX^*5MOX1)#h5QbxWomwpd>sSATr+CAE3<vD>18esyC$6B)C(WAfxJ&3!_hvxMt#N;i|l%B6H?@jlurV4&difZha23CqTA<A@t)3pk)+!X4WrA8MslX3o`TN^?7njF0s;Z=7Q|#ISpOY*XcKrSbIuD`Kk%6GrQLC1*VBV=ZkBV<O^{DTDil{8j}Lj!`sEr$y%6MjeiLZ7>M3c_TxYPNZylYJ2QTAwZwENoCI<99};pv4!fQ1K+yhpb{~N`XS#`n+oVkZP}lm<EzH&_d|l079!VYn^F$o^cW9jtf9c(l",
    "Part4": "7SB6SA`?N-y_HX@x-(PA5Q;Ba;77#6I;uH%G*h#MPEr&st7P6I4S@EYiy?7|cVP>8`ok4%kc=o7&6=;Mtqm1%+nmhiNXi+7Ub5cVhz<t;xo8Q}2EyF!n)S0y!^%Le>kxFiJ3QYSW_4D40$PZ4xTuZ%UH$<li8{N(Faf1U)?4-GZ5g_4p4a0HCpVgWeB+uUqh#(TB+s4u^;~yhcSF5PGq?WE%GkaFnq<QJHgk>b1<!H>y5Zv$`T3l#{<pwTc!UxWhD5+PnYxTt^*LlXGgiB&q=ME+pg4f?=HX3e%ez|u=u{n1GW`~d7Ec#FwOJk(_|S0``;In{ouvEbwi&1kSp$<gyS2BL%7Y$MfA7r{gQg4|9h%@9S%ToVmHfxf!}_3JOCiDZ@aH%x3EB*mmhe67973=9rxLR!@5Mk(K;>Fd@iO;hT!LZ1_L5ta=GZHJU>}6&e0{H4K_2|4A>!QJj8EC+_KxA1jt(0Pq=!)X7{KCCIXeJ94Gc}$aDRN@|Hq4d2;X8Z+P6wS7r=u-C_1|*CQ_p3Fu?YGW$4|(`mmIs00rZyhV_-$NM%r-Vfn4^S9{$f@Z}QdSpn+j3Q%OaL!-XH(7a!FrB%$l0vGxtR40w%bYO*Y{3v@J6@HTnzLwvG%~-;Y|Ewuv^zI<1ld`@}oh^gIaWJ=#-e#gX=C}|p=%=Vjq(qpE<93WdRxdLpkx`7OP3vu~Lys(S_SkGZf2O=nfYcu7C`eH)U3KEbc&nCaz&L1IUfA=3;f<Ma#Eee^fx0@M@aAvuC5KvkS+56uHOe>i{^I-^uB}7g)hqm`0KUc{br^XWr`$uSe5PVTYnu-<2%k5@B_c%3id2Pe?{j-=CX?l2!3SM05!3&HxJxucrw^IWnhh99AL`4IZYp`A&#J5SCZ^j@)U72Ddt9S74&X7prQ6-s6W{9(@h7i=+X^!gO<wOSi;el-*}5nvEEWznHw{0mcb+SxN0sO<f?TzSrGg|XI!U*P!u+XcO43HS2IbEijYTMX+dGJ5g3y1^!mA*MBhiHiCFjVfHOUvNG&-RfKfNZdm5{s88y!kh`RoDExq51BL&yAC*~um~1`WA&7DPHkJaEvy>4-3d2prqlx4aT6*h}8>Z7boAd*VG$$tcfeSZ2Zx|2Ho0C3@Iq(2Reu$<<^KQHk0cD~Xn6|E4L-#x-H!snVI|<+~NE*nI3e1qi9EXel9it+$1i#rIsV_W5kCH)F*t_(X=5(8$mOqQo(7s?&yb$5I7CZ`WIYIy~QUFbI=Pw|@BKQ7qD%yYNdSfAH&yT+fG0#xV#}&AX>rxssLk<UmG5%k}b`6NL9a!zGt6U=iRS7!G(9IA$aXBjN~HU>lu0@NPyaVpQN_2#<~vA?4oh8^R_|-x!rcq*@4vWju3YiKymwQx!$^*@DXEO+{fGirXs@RRTWS#7u!cdaBH-3|deoUgEEJG9+5-X;}K%nYW(aU*si+54-3%iMHyA0vTO=3ov%mNzPraaBK9ktZ0T0sr-?89Ju@6!Ov^2`pvv^W<ED0S7-wd`DFj|sI@dA8vM2;75Rv@3`UOa^W}T|$>_VbUV!9|?iTz#$j1t6cHHz_(EGLrP8bhJ%g@(-p~+OfBf|3%^u!yutUx0apBxdp4doDEpM|VyM*Eqz3riWU>xH2tDcAW2mpTCZint`eW}0=ayhRqiRMm-8hs%&Dwea6roTa5nZpj-a*2Lv!EhGz0UkG{Z*z)YSTxd5$IbxY(`kBgY-aZ4=2BLqhf8X2^abbi?UWgSTuP^Kj%#E{b0t;*n-s~x;qT{wb0YdP0arKcV0cXavnhLG+jvhqxg!Z&#7JhWsY=u_clpoUduFR~XFth_IfFsE(;(-}{(@isFAw>s{!ys(lHmNIY8G8Xc1FWUD&baSp3=Nd8s|FgP*oqzqste+!_|IrDJOT!)!*9L;MfXCQZ66an&%qjrlpCVhx)w5pYnj`NF>cZcmn3=MR0|Rwie(Q@_+Ko~M=RogaTS<=bxGZugUuUKLPp9!RHigkC#avB&_3F7=|w9>j#Ho%k)KfdR@$LV8-v!BKeE)jk&fqu^bU=D$%_+q&%+P;U?wf`h!&9F9ecQ_E$?n8HjJuXy_iz|w#hqj>3q_+Ro>=UUL*_+w8Y7o5VKhrjE>*2SN$Eskh~K-d1H!tG%duPKfhB8tOW`17t>Z?>4a(uN$(9{<o_(Wh}ZyxK~(Xnx6%}_O__bpVBzWIPZH_T5*v{=NLm&iN|$ynS#*3qv(ljiy@1MRgCo=4I8!f$PEyGl_+)A=W0|zv-(T#dwMmQ$l3%LqhOp-Gvb-cLasp~AyQ|q!&*^`0=%W|2T1)L6#b2_OwnXGhConQ*Fo59Al9#pW{i5ZmZMvaNQ0)KvSA@yB3g&@U5ZWZAIHGH!TQU?!+UD||{sGMm=O?3P4;=P&p}8d0_Bt^DD&CU57XCsyXQzU$OhW=4xZuT}KcH#<_s1P+%l1dFPQ94RR&%`g<#S`l%be9|g*N7`w3!>&sLB=N*PnuI=hPLML>;3Cw;OAz8Zy>Ib687+%@826=#(ia@yUClbhjQ)ID)4~AS7!iGB>ZbPp(m~WxtO+KLCll=Vje7h2f5d=@$g@-LG^lU;)V=>IDd7+Q9bs$4!VUU&$p&;0p*^QBEYPNK)WvQEy_7W`;%agrXJc9gw!dWf*x0!8TN|g<pUxKrfGqHKRD9;A-?Na`_2eSFZrjmwAzZSy+94MtDD@7iJjblbQekW5`3Z00G=vfWQI(s<f)7J}?c70ssI200CKA"
   }
  }
 },
 "Resources": {
  "AppServerA": {
   "Type": "AWS::EC2::Instance",
   "Properties": {
    "ImageId": {
     "Ref": "LatestAmiId"
    },
    "InstanceType": {
     "Ref": "InstanceType"
    },
    "IamInstanceProfile": {
     "Ref": "InstanceProfile"
    },
    "NetworkInterfaces": [
     {
      "DeviceIndex": "0",
      "SubnetId": {
       "Ref": "AppSubnetA"
      },
      "GroupSet": [
       {
        "Ref": "AppSecurityGroup"
       }
      ],
      "AssociatePublicIpAddress": false,
      "DeleteOnTermination": true
     }
    ],
    "MetadataOptions": {
     "HttpTokens": "required",
     "HttpEndpoint": "enabled",
     "HttpPutResponseHopLimit": 2
    },
    "UserData": {
     "Fn::Base64": {
      "Fn::Join": [
       "",
       [
        "#!/bin/bash\n# INFS3701 Campus Cafe - app server A (private app subnet)\n# The block below is the cafe app (Python program, web page and installer), packed with tar + xz + base85.\n# Setup log: /var/log/cloud-init-output.log    Service: systemctl status cafe-app\nmkdir -p /opt/cafe/src\npython3 -c \"import base64,io,lzma,sys,tarfile;tarfile.open(fileobj=io.BytesIO(lzma.decompress(base64.b85decode(''.join(sys.stdin.read().split()))))).extractall('/opt/cafe/src')\" <<'CAFE_BUNDLE'\n",
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part1"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part2"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part3"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part4"
         ]
        },
        "\nCAFE_BUNDLE\nbash /opt/cafe/src/install.sh app",
        "\n"
       ]
      ]
     }
    },
    "Tags": [
     {
      "Key": "Name",
      "Value": "cafe-app-a"
     },
     {
      "Key": "Project",
      "Value": "INFS3701-cafe"
     }
    ]
   }
  },
  "WebServerA": {
   "Type": "AWS::EC2::Instance",
   "Properties": {
    "ImageId": {
     "Ref": "LatestAmiId"
    },
    "InstanceType": {
     "Ref": "InstanceType"
    },
    "IamInstanceProfile": {
     "Ref": "InstanceProfile"
    },
    "NetworkInterfaces": [
     {
      "DeviceIndex": "0",
      "SubnetId": {
       "Ref": "PublicSubnetA"
      },
      "GroupSet": [
       {
        "Ref": "WebSecurityGroup"
       }
      ],
      "AssociatePublicIpAddress": true,
      "DeleteOnTermination": true
     }
    ],
    "MetadataOptions": {
     "HttpTokens": "required",
     "HttpEndpoint": "enabled",
     "HttpPutResponseHopLimit": 2
    },
    "UserData": {
     "Fn::Base64": {
      "Fn::Join": [
       "",
       [
        "#!/bin/bash\n# INFS3701 Campus Cafe - web server A (public subnet)\n# The block below is the cafe app (Python program, web page and installer), packed with tar + xz + base85.\n# Setup log: /var/log/cloud-init-output.log    Service: systemctl status cafe-web\nmkdir -p /opt/cafe/src\npython3 -c \"import base64,io,lzma,sys,tarfile;tarfile.open(fileobj=io.BytesIO(lzma.decompress(base64.b85decode(''.join(sys.stdin.read().split()))))).extractall('/opt/cafe/src')\" <<'CAFE_BUNDLE'\n",
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part1"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part2"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part3"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part4"
         ]
        },
        "\nCAFE_BUNDLE\nbash /opt/cafe/src/install.sh web",
        " --upstream ",
        {
         "Fn::GetAtt": [
          "AppServerA",
          "PrivateIp"
         ]
        },
        "\n"
       ]
      ]
     }
    },
    "Tags": [
     {
      "Key": "Name",
      "Value": "cafe-web-a"
     },
     {
      "Key": "Project",
      "Value": "INFS3701-cafe"
     }
    ]
   }
  },
  "AppServerB": {
   "Type": "AWS::EC2::Instance",
   "Properties": {
    "ImageId": {
     "Ref": "LatestAmiId"
    },
    "InstanceType": {
     "Ref": "InstanceType"
    },
    "IamInstanceProfile": {
     "Ref": "InstanceProfile"
    },
    "NetworkInterfaces": [
     {
      "DeviceIndex": "0",
      "SubnetId": {
       "Ref": "AppSubnetB"
      },
      "GroupSet": [
       {
        "Ref": "AppSecurityGroup"
       }
      ],
      "AssociatePublicIpAddress": false,
      "DeleteOnTermination": true
     }
    ],
    "MetadataOptions": {
     "HttpTokens": "required",
     "HttpEndpoint": "enabled",
     "HttpPutResponseHopLimit": 2
    },
    "UserData": {
     "Fn::Base64": {
      "Fn::Join": [
       "",
       [
        "#!/bin/bash\n# INFS3701 Campus Cafe - app server B (private app subnet)\n# The block below is the cafe app (Python program, web page and installer), packed with tar + xz + base85.\n# Setup log: /var/log/cloud-init-output.log    Service: systemctl status cafe-app\nmkdir -p /opt/cafe/src\npython3 -c \"import base64,io,lzma,sys,tarfile;tarfile.open(fileobj=io.BytesIO(lzma.decompress(base64.b85decode(''.join(sys.stdin.read().split()))))).extractall('/opt/cafe/src')\" <<'CAFE_BUNDLE'\n",
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part1"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part2"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part3"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part4"
         ]
        },
        "\nCAFE_BUNDLE\nbash /opt/cafe/src/install.sh app",
        "\n"
       ]
      ]
     }
    },
    "Tags": [
     {
      "Key": "Name",
      "Value": "cafe-app-b"
     },
     {
      "Key": "Project",
      "Value": "INFS3701-cafe"
     }
    ]
   }
  },
  "WebServerB": {
   "Type": "AWS::EC2::Instance",
   "Properties": {
    "ImageId": {
     "Ref": "LatestAmiId"
    },
    "InstanceType": {
     "Ref": "InstanceType"
    },
    "IamInstanceProfile": {
     "Ref": "InstanceProfile"
    },
    "NetworkInterfaces": [
     {
      "DeviceIndex": "0",
      "SubnetId": {
       "Ref": "PublicSubnetB"
      },
      "GroupSet": [
       {
        "Ref": "WebSecurityGroup"
       }
      ],
      "AssociatePublicIpAddress": true,
      "DeleteOnTermination": true
     }
    ],
    "MetadataOptions": {
     "HttpTokens": "required",
     "HttpEndpoint": "enabled",
     "HttpPutResponseHopLimit": 2
    },
    "UserData": {
     "Fn::Base64": {
      "Fn::Join": [
       "",
       [
        "#!/bin/bash\n# INFS3701 Campus Cafe - web server B (public subnet)\n# The block below is the cafe app (Python program, web page and installer), packed with tar + xz + base85.\n# Setup log: /var/log/cloud-init-output.log    Service: systemctl status cafe-web\nmkdir -p /opt/cafe/src\npython3 -c \"import base64,io,lzma,sys,tarfile;tarfile.open(fileobj=io.BytesIO(lzma.decompress(base64.b85decode(''.join(sys.stdin.read().split()))))).extractall('/opt/cafe/src')\" <<'CAFE_BUNDLE'\n",
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part1"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part2"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part3"
         ]
        },
        {
         "Fn::FindInMap": [
          "CafeApp",
          "Bundle",
          "Part4"
         ]
        },
        "\nCAFE_BUNDLE\nbash /opt/cafe/src/install.sh web",
        " --upstream ",
        {
         "Fn::GetAtt": [
          "AppServerB",
          "PrivateIp"
         ]
        },
        "\n"
       ]
      ]
     }
    },
    "Tags": [
     {
      "Key": "Name",
      "Value": "cafe-web-b"
     },
     {
      "Key": "Project",
      "Value": "INFS3701-cafe"
     }
    ]
   }
  }
 },
 "Outputs": {
  "CafeURLA": {
   "Description": "Open the cafe through web server A",
   "Value": {
    "Fn::Join": [
     "",
     [
      "http://",
      {
       "Fn::GetAtt": [
        "WebServerA",
        "PublicIp"
       ]
      }
     ]
    ]
   }
  },
  "AppServerAPrivateIp": {
   "Description": "cafe-app-a private IP",
   "Value": {
    "Fn::GetAtt": [
     "AppServerA",
     "PrivateIp"
    ]
   }
  },
  "AppServerA": {
   "Description": "cafe-app-a instance ID",
   "Value": {
    "Ref": "AppServerA"
   }
  },
  "WebServerA": {
   "Description": "cafe-web-a instance ID",
   "Value": {
    "Ref": "WebServerA"
   }
  },
  "CafeURLB": {
   "Description": "Open the cafe through web server B",
   "Value": {
    "Fn::Join": [
     "",
     [
      "http://",
      {
       "Fn::GetAtt": [
        "WebServerB",
        "PublicIp"
       ]
      }
     ]
    ]
   }
  },
  "AppServerBPrivateIp": {
   "Description": "cafe-app-b private IP",
   "Value": {
    "Fn::GetAtt": [
     "AppServerB",
     "PrivateIp"
    ]
   }
  },
  "AppServerB": {
   "Description": "cafe-app-b instance ID",
   "Value": {
    "Ref": "AppServerB"
   }
  },
  "WebServerB": {
   "Description": "cafe-web-b instance ID",
   "Value": {
    "Ref": "WebServerB"
   }
  },
  "ConnectAppServersToDatabase": {
   "Description": "Week 8: after creating the database, run this on each app server (Session Manager): sudo cafe-connect-db --host DB_ENDPOINT --secret-arn SECRET_ARN --copy-local-orders  (or --user NAME instead of --secret-arn to type a password; --help for more)",
   "Value": "sudo cafe-connect-db --host DB_ENDPOINT --secret-arn SECRET_ARN --copy-local-orders"
  }
 },
 "Rules": {
  "DifferentSubnets": {
   "Assertions": [
    {
     "Assert": {
      "Fn::Not": [
       {
        "Fn::Equals": [
         {
          "Ref": "PublicSubnetA"
         },
         {
          "Ref": "PublicSubnetB"
         }
        ]
       }
      ]
     },
     "AssertDescription": "Choose two different public subnets (one per zone)."
    },
    {
     "Assert": {
      "Fn::Not": [
       {
        "Fn::Equals": [
         {
          "Ref": "AppSubnetA"
         },
         {
          "Ref": "AppSubnetB"
         }
        ]
       }
      ]
     },
     "AssertDescription": "Choose two different private app subnets (one per zone)."
    }
   ]
  }
 }
}
```
