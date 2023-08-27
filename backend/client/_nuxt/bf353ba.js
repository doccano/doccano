(window.webpackJsonp=window.webpackJsonp||[]).push([[24],{1117:function(t,e,o){"use strict";o.r(e);var n=o(1),f=(o(21),o(31),o(139),o(7),o(26),o(131),o(111),o(0)),r=o(773),c=f.default.extend({layout:"project",middleware:["check-auth","auth","setCurrentProject","isProjectAdmin"],validate:function(t){var e=t.params;return/^\d+$/.test(e.id)},data:function(){return{exportApproved:!1,file:null,fileFormatRules:r.a,formats:[],isProcessing:!1,polling:null,selectedFormat:null,taskId:"",valid:!1}},computed:{projectId:function(){return this.$route.params.id},example:function(){var t=this;return this.formats.find((function(e){return e.name===t.selectedFormat})).example.trim()}},created:function(){var t=this;return Object(n.a)(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,t.$repositories.downloadFormat.list(t.projectId);case 2:t.formats=e.sent;case 3:case"end":return e.stop()}}),e)})))()},beforeDestroy:function(){clearInterval(this.polling)},methods:{reset:function(){this.$refs.form.reset(),this.taskId="",this.exportApproved=!1,this.selectedFormat=null,this.isProcessing=!1},downloadRequest:function(){var t=this;return Object(n.a)(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t.isProcessing=!0,e.next=3,t.$repositories.download.prepare(t.projectId,t.selectedFormat,t.exportApproved);case 3:t.taskId=e.sent,t.pollData();case 5:case"end":return e.stop()}}),e)})))()},pollData:function(){var t=this;this.polling=setInterval(Object(n.a)(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!t.taskId){e.next=5;break}return e.next=3,t.$repositories.taskStatus.get(t.taskId);case 3:e.sent.ready&&(t.$repositories.download.download(t.projectId,t.taskId),t.reset());case 5:case"end":return e.stop()}}),e)}))),1e3)}}}),l=o(86),d=o(90),m=o.n(d),h=o(326),w=o(683),y=o(677),v=o(784),R=o(736),O=o(319),x=o(215),j=o(682),_=o(122),component=Object(l.a)(c,(function(){var t=this,e=t._self._c;t._self._setupProxy;return e("v-card",[e("v-card-title",[t._v("\n    "+t._s(t.$t("dataset.exportDataTitle"))+"\n  ")]),t._v(" "),e("v-card-text",[e("v-overlay",{attrs:{value:t.isProcessing}},[e("v-progress-circular",{attrs:{indeterminate:"",size:"64"}})],1),t._v(" "),e("v-form",{ref:"form",model:{value:t.valid,callback:function(e){t.valid=e},expression:"valid"}},[e("v-select",{attrs:{items:t.formats,"hide-details":"auto","item-text":"name",label:"File format",outlined:"",rules:t.fileFormatRules(t.$t("rules.fileFormatRules"))},model:{value:t.selectedFormat,callback:function(e){t.selectedFormat=e},expression:"selectedFormat"}}),t._v(" "),t.selectedFormat?e("v-sheet",{staticClass:"mt-2 pa-5",attrs:{dark:!t.$vuetify.theme.dark,light:t.$vuetify.theme.dark}},[e("pre",[t._v(t._s(t.example))])]):t._e(),t._v(" "),e("v-checkbox",{attrs:{label:"Export only approved documents","hide-details":""},model:{value:t.exportApproved,callback:function(e){t.exportApproved=e},expression:"exportApproved"}})],1)],1),t._v(" "),e("v-card-actions",[e("v-btn",{staticClass:"text-capitalize ms-2 primary",attrs:{disabled:!t.valid},on:{click:t.downloadRequest}},[t._v("\n      "+t._s(t.$t("generic.export"))+"\n    ")])],1)],1)}),[],!1,null,null,null);e.default=component.exports;m()(component,{VBtn:h.a,VCard:w.a,VCardActions:y.a,VCardText:y.b,VCardTitle:y.c,VCheckbox:v.a,VForm:R.a,VOverlay:O.a,VProgressCircular:x.a,VSelect:j.a,VSheet:_.a})},677:function(t,e,o){"use strict";o.d(e,"a",(function(){return r})),o.d(e,"b",(function(){return l})),o.d(e,"c",(function(){return d}));var n=o(683),f=o(4),r=Object(f.j)("v-card__actions"),c=Object(f.j)("v-card__subtitle"),l=Object(f.j)("v-card__text"),d=Object(f.j)("v-card__title");n.a},736:function(t,e,o){"use strict";var n=o(5),f=(o(93),o(106),o(273),o(11),o(7),o(13),o(111),o(139),o(12),o(10),o(16),o(17),o(14)),r=o(148),c=o(168);function l(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(object);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,o)}return e}function d(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?l(Object(source),!0).forEach((function(e){Object(n.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):l(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}e.a=Object(f.a)(r.a,Object(c.b)("form")).extend({name:"v-form",provide:function(){return{form:this}},inheritAttrs:!1,props:{disabled:Boolean,lazyValidation:Boolean,readonly:Boolean,value:Boolean},data:function(){return{inputs:[],watchers:[],errorBag:{}}},watch:{errorBag:{handler:function(t){var e=Object.values(t).includes(!0);this.$emit("input",!e)},deep:!0,immediate:!0}},methods:{watchInput:function(input){var t=this,e=function(input){return input.$watch("hasError",(function(e){t.$set(t.errorBag,input._uid,e)}),{immediate:!0})},o={_uid:input._uid,valid:function(){},shouldValidate:function(){}};return this.lazyValidation?o.shouldValidate=input.$watch("shouldValidate",(function(n){n&&(t.errorBag.hasOwnProperty(input._uid)||(o.valid=e(input)))})):o.valid=e(input),o},validate:function(){return 0===this.inputs.filter((function(input){return!input.validate(!0)})).length},reset:function(){this.inputs.forEach((function(input){return input.reset()})),this.resetErrorBag()},resetErrorBag:function(){var t=this;this.lazyValidation&&setTimeout((function(){t.errorBag={}}),0)},resetValidation:function(){this.inputs.forEach((function(input){return input.resetValidation()})),this.resetErrorBag()},register:function(input){this.inputs.push(input),this.watchers.push(this.watchInput(input))},unregister:function(input){var t=this.inputs.find((function(i){return i._uid===input._uid}));if(t){var e=this.watchers.find((function(i){return i._uid===t._uid}));e&&(e.valid(),e.shouldValidate()),this.watchers=this.watchers.filter((function(i){return i._uid!==t._uid})),this.inputs=this.inputs.filter((function(i){return i._uid!==t._uid})),this.$delete(this.errorBag,t._uid)}}},render:function(t){var e=this;return t("form",{staticClass:"v-form",attrs:d({novalidate:!0},this.attrs$),on:{submit:function(t){return e.$emit("submit",t)}}},this.$slots.default)}})},756:function(t,e,o){var content=o(757);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,o(30).default)("73967b04",content,!0,{sourceMap:!1})},757:function(t,e,o){var n=o(29),f=o(33),r=o(34),c=o(35),l=o(36),d=o(37),m=o(38),h=o(39),w=o(40),y=o(41),v=o(42),R=o(43),O=o(44),x=o(45),j=o(46),_=o(47),k=o(48),I=o(49),$=o(50),P=o(51),V=o(52),C=o(53),B=o(54),S=o(55),F=o(56),D=o(57),E=o(58),A=o(59),T=o(60),z=o(61),L=o(62),M=o(63),N=o(64),J=o(65),G=o(66),H=o(67),K=o(68),Q=o(69),U=o(70),W=o(71),X=o(72),Y=o(73),Z=o(74),tt=o(75),et=n((function(i){return i[1]})),ot=f(r),nt=f(c),ft=f(l),at=f(d),ut=f(m),it=f(h),st=f(w),ct=f(y),lt=f(v),pt=f(R),mt=f(O),ht=f(x),bt=f(j),wt=f(_),yt=f(k),gt=f(I),vt=f($),Rt=f(P),Ot=f(V),xt=f(C),jt=f(B),_t=f(S),kt=f(F),It=f(D),$t=f(E),Pt=f(A),Vt=f(T),Ct=f(z),Bt=f(L),St=f(M),Ft=f(N),Dt=f(J),Et=f(G),At=f(H),Tt=f(K),qt=f(Q),zt=f(U),Lt=f(W),Mt=f(X),Nt=f(Y),Jt=f(Z),Gt=f(tt);et.push([t.i,'@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:100;src:url('+ot+') format("woff2");unicode-range:u+0460-052f,u+1c80-1c88,u+20b4,u+2de0-2dff,u+a640-a69f,u+fe2e-fe2f}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:100;src:url('+nt+') format("woff2");unicode-range:u+0301,u+0400-045f,u+0490-0491,u+04b0-04b1,u+2116}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:100;src:url('+ft+') format("woff2");unicode-range:u+1f??}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:100;src:url('+at+') format("woff2");unicode-range:u+0370-03ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:100;src:url('+ut+') format("woff2");unicode-range:u+0102-0103,u+0110-0111,u+0128-0129,u+0168-0169,u+01a0-01a1,u+01af-01b0,u+0300-0301,u+0303-0304,u+0308-0309,u+0323,u+0329,u+1ea0-1ef9,u+20ab}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:100;src:url('+it+') format("woff2");unicode-range:u+0100-02af,u+0304,u+0308,u+0329,u+1e00-1e9f,u+1ef2-1eff,u+2020,u+20a0-20ab,u+20ad-20cf,u+2113,u+2c60-2c7f,u+a720-a7ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:100;src:url('+st+') format("woff2");unicode-range:u+00??,u+0131,u+0152-0153,u+02bb-02bc,u+02c6,u+02da,u+02dc,u+0304,u+0308,u+0329,u+2000-206f,u+2074,u+20ac,u+2122,u+2191,u+2193,u+2212,u+2215,u+feff,u+fffd}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:300;src:url('+ct+') format("woff2");unicode-range:u+0460-052f,u+1c80-1c88,u+20b4,u+2de0-2dff,u+a640-a69f,u+fe2e-fe2f}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:300;src:url('+lt+') format("woff2");unicode-range:u+0301,u+0400-045f,u+0490-0491,u+04b0-04b1,u+2116}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:300;src:url('+pt+') format("woff2");unicode-range:u+1f??}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:300;src:url('+mt+') format("woff2");unicode-range:u+0370-03ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:300;src:url('+ht+') format("woff2");unicode-range:u+0102-0103,u+0110-0111,u+0128-0129,u+0168-0169,u+01a0-01a1,u+01af-01b0,u+0300-0301,u+0303-0304,u+0308-0309,u+0323,u+0329,u+1ea0-1ef9,u+20ab}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:300;src:url('+bt+') format("woff2");unicode-range:u+0100-02af,u+0304,u+0308,u+0329,u+1e00-1e9f,u+1ef2-1eff,u+2020,u+20a0-20ab,u+20ad-20cf,u+2113,u+2c60-2c7f,u+a720-a7ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:300;src:url('+wt+') format("woff2");unicode-range:u+00??,u+0131,u+0152-0153,u+02bb-02bc,u+02c6,u+02da,u+02dc,u+0304,u+0308,u+0329,u+2000-206f,u+2074,u+20ac,u+2122,u+2191,u+2193,u+2212,u+2215,u+feff,u+fffd}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:400;src:url('+yt+') format("woff2");unicode-range:u+0460-052f,u+1c80-1c88,u+20b4,u+2de0-2dff,u+a640-a69f,u+fe2e-fe2f}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:400;src:url('+gt+') format("woff2");unicode-range:u+0301,u+0400-045f,u+0490-0491,u+04b0-04b1,u+2116}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:400;src:url('+vt+') format("woff2");unicode-range:u+1f??}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:400;src:url('+Rt+') format("woff2");unicode-range:u+0370-03ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:400;src:url('+Ot+') format("woff2");unicode-range:u+0102-0103,u+0110-0111,u+0128-0129,u+0168-0169,u+01a0-01a1,u+01af-01b0,u+0300-0301,u+0303-0304,u+0308-0309,u+0323,u+0329,u+1ea0-1ef9,u+20ab}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:400;src:url('+xt+') format("woff2");unicode-range:u+0100-02af,u+0304,u+0308,u+0329,u+1e00-1e9f,u+1ef2-1eff,u+2020,u+20a0-20ab,u+20ad-20cf,u+2113,u+2c60-2c7f,u+a720-a7ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:400;src:url('+jt+') format("woff2");unicode-range:u+00??,u+0131,u+0152-0153,u+02bb-02bc,u+02c6,u+02da,u+02dc,u+0304,u+0308,u+0329,u+2000-206f,u+2074,u+20ac,u+2122,u+2191,u+2193,u+2212,u+2215,u+feff,u+fffd}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:500;src:url('+_t+') format("woff2");unicode-range:u+0460-052f,u+1c80-1c88,u+20b4,u+2de0-2dff,u+a640-a69f,u+fe2e-fe2f}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:500;src:url('+kt+') format("woff2");unicode-range:u+0301,u+0400-045f,u+0490-0491,u+04b0-04b1,u+2116}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:500;src:url('+It+') format("woff2");unicode-range:u+1f??}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:500;src:url('+$t+') format("woff2");unicode-range:u+0370-03ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:500;src:url('+Pt+') format("woff2");unicode-range:u+0102-0103,u+0110-0111,u+0128-0129,u+0168-0169,u+01a0-01a1,u+01af-01b0,u+0300-0301,u+0303-0304,u+0308-0309,u+0323,u+0329,u+1ea0-1ef9,u+20ab}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:500;src:url('+Vt+') format("woff2");unicode-range:u+0100-02af,u+0304,u+0308,u+0329,u+1e00-1e9f,u+1ef2-1eff,u+2020,u+20a0-20ab,u+20ad-20cf,u+2113,u+2c60-2c7f,u+a720-a7ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:500;src:url('+Ct+') format("woff2");unicode-range:u+00??,u+0131,u+0152-0153,u+02bb-02bc,u+02c6,u+02da,u+02dc,u+0304,u+0308,u+0329,u+2000-206f,u+2074,u+20ac,u+2122,u+2191,u+2193,u+2212,u+2215,u+feff,u+fffd}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:700;src:url('+Bt+') format("woff2");unicode-range:u+0460-052f,u+1c80-1c88,u+20b4,u+2de0-2dff,u+a640-a69f,u+fe2e-fe2f}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:700;src:url('+St+') format("woff2");unicode-range:u+0301,u+0400-045f,u+0490-0491,u+04b0-04b1,u+2116}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:700;src:url('+Ft+') format("woff2");unicode-range:u+1f??}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:700;src:url('+Dt+') format("woff2");unicode-range:u+0370-03ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:700;src:url('+Et+') format("woff2");unicode-range:u+0102-0103,u+0110-0111,u+0128-0129,u+0168-0169,u+01a0-01a1,u+01af-01b0,u+0300-0301,u+0303-0304,u+0308-0309,u+0323,u+0329,u+1ea0-1ef9,u+20ab}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:700;src:url('+At+') format("woff2");unicode-range:u+0100-02af,u+0304,u+0308,u+0329,u+1e00-1e9f,u+1ef2-1eff,u+2020,u+20a0-20ab,u+20ad-20cf,u+2113,u+2c60-2c7f,u+a720-a7ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:700;src:url('+Tt+') format("woff2");unicode-range:u+00??,u+0131,u+0152-0153,u+02bb-02bc,u+02c6,u+02da,u+02dc,u+0304,u+0308,u+0329,u+2000-206f,u+2074,u+20ac,u+2122,u+2191,u+2193,u+2212,u+2215,u+feff,u+fffd}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:900;src:url('+qt+') format("woff2");unicode-range:u+0460-052f,u+1c80-1c88,u+20b4,u+2de0-2dff,u+a640-a69f,u+fe2e-fe2f}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:900;src:url('+zt+') format("woff2");unicode-range:u+0301,u+0400-045f,u+0490-0491,u+04b0-04b1,u+2116}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:900;src:url('+Lt+') format("woff2");unicode-range:u+1f??}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:900;src:url('+Mt+') format("woff2");unicode-range:u+0370-03ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:900;src:url('+Nt+') format("woff2");unicode-range:u+0102-0103,u+0110-0111,u+0128-0129,u+0168-0169,u+01a0-01a1,u+01af-01b0,u+0300-0301,u+0303-0304,u+0308-0309,u+0323,u+0329,u+1ea0-1ef9,u+20ab}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:900;src:url('+Jt+') format("woff2");unicode-range:u+0100-02af,u+0304,u+0308,u+0329,u+1e00-1e9f,u+1ef2-1eff,u+2020,u+20a0-20ab,u+20ad-20cf,u+2113,u+2c60-2c7f,u+a720-a7ff}@font-face{font-display:swap;font-family:"Roboto";font-style:normal;font-weight:900;src:url('+Gt+') format("woff2");unicode-range:u+00??,u+0131,u+0152-0153,u+02bb-02bc,u+02c6,u+02da,u+02dc,u+0304,u+0308,u+0329,u+2000-206f,u+2074,u+20ac,u+2122,u+2191,u+2193,u+2212,u+2215,u+feff,u+fffd}.v-input--checkbox.v-input--indeterminate.v-input--is-disabled{opacity:.6}.v-input--checkbox.v-input--dense{margin-top:4px}',""]),et.locals={},t.exports=et},773:function(t,e,o){"use strict";o.d(e,"b",(function(){return n})),o.d(e,"f",(function(){return f})),o.d(e,"a",(function(){return r})),o.d(e,"e",(function(){return c})),o.d(e,"c",(function(){return l})),o.d(e,"d",(function(){return d}));o(7);var n=function(t){return[function(e){return!!e||t.labelRequired},function(e){return e&&e.length<=30||t.labelLessThan30Chars}]},f=function(t){return[function(e){return!!e||t.userNameRequired},function(e){return e&&e.length<=30||t.userNameLessThan30Chars}]},r=function(t){return[function(e){return!!e||t.fileFormatRequired}]},c=function(t){return[function(e){return!!e||t.fileRequired},function(e){return!e||e.size<1e6||t.fileLessThan1MB}]},l=function(t){return[function(e){return!!e||t.passwordRequired},function(e){return e&&e.length<=30||t.passwordLessThan30Chars}]},d=function(){return[function(t){return!!t||"Name is required"}]}},784:function(t,e,o){"use strict";o(12),o(10),o(11),o(16),o(13),o(17);var n=o(141),f=o(5),r=(o(7),o(82),o(756),o(440),o(135)),c=o(198),l=o(350),d=["title"];function m(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(object);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,o)}return e}function h(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?m(Object(source),!0).forEach((function(e){Object(f.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):m(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}e.a=l.a.extend({name:"v-checkbox",props:{indeterminate:Boolean,indeterminateIcon:{type:String,default:"$checkboxIndeterminate"},offIcon:{type:String,default:"$checkboxOff"},onIcon:{type:String,default:"$checkboxOn"}},data:function(){return{inputIndeterminate:this.indeterminate}},computed:{classes:function(){return h(h({},c.a.options.computed.classes.call(this)),{},{"v-input--selection-controls":!0,"v-input--checkbox":!0,"v-input--indeterminate":this.inputIndeterminate})},computedIcon:function(){return this.inputIndeterminate?this.indeterminateIcon:this.isActive?this.onIcon:this.offIcon},validationState:function(){if(!this.isDisabled||this.inputIndeterminate)return this.hasError&&this.shouldValidate?"error":this.hasSuccess?"success":null!==this.hasColor?this.computedColor:void 0}},watch:{indeterminate:function(t){var e=this;this.$nextTick((function(){return e.inputIndeterminate=t}))},inputIndeterminate:function(t){this.$emit("update:indeterminate",t)},isActive:function(){this.indeterminate&&(this.inputIndeterminate=!1)}},methods:{genCheckbox:function(){var t=this.attrs$,e=(t.title,Object(n.a)(t,d));return this.$createElement("div",{staticClass:"v-input--selection-controls__input"},[this.$createElement(r.a,this.setTextColor(this.validationState,{props:{dense:this.dense,dark:this.dark,light:this.light}}),this.computedIcon),this.genInput("checkbox",h(h({},e),{},{"aria-checked":this.inputIndeterminate?"mixed":this.isActive.toString()})),this.genRipple(this.setTextColor(this.rippleState))])},genDefaultSlot:function(){return[this.genCheckbox(),this.genLabel()]}}})}}]);