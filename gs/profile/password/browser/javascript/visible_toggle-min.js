jQuery.noConflict();function GSProfilePasswordToggle(e,a){var i=null,f=null,d=false;
function g(){i.attr("type","text");d=true}function c(){i.attr("type","password");
d=false}function h(){return visibile}function b(){d=!d;if(d){g()}else{c()}}function j(){i=jQuery(e);
f=jQuery(a);d=Boolean(Number(f.val()));try{if(d){g()}else{c()}f.change(b)}catch(k){f.hide();
f.next("label").hide()}}j();return{get_visibility:function(){return h()},}};