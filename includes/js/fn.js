var previous_id = 0;
if(typeof(struc) !== "undefined") // Is data set
{
	document.title = struc.site_name; // Change site name
	$(function(){ // Onload
		console.info("Try this code [↑ ↑ ↓ ↓  ← → ← → i s n] and see what happens !")
		$("#home_title").html(struc.home_title); // Change big text
		$('head link:last').before('<link rel="stylesheet" href="includes/css/syntax_highlighter/'+struc.code_color+'.css" type="text/css" />');
		if($('#page_ctn').is(':empty')){
			loadmd(0,true);
		}
		for (var i = menu.length - 1; i >= 0; i--) {
			$("#menu").prepend("<button type=\"button\" class=\"btn btn-info\" onclick='loadmd(\""+i+"\");return false;'>"+menu[i].name+"</button> ");
		};
		$("#page_ctn").hover(function(){
			$("#header").slideUp();
		});
		$("#page_ctn").mouseleave(function(){
			var scr = f_scrollTop();
			if(scr <= 48)
			{
				$("#header").slideDown();
			}
		});
	});
}

function loadmd(id,isdefault)
{
	loc = menu[id].location;
	console.log("Pre -> "+previous_id+" | This id "+id);

	if(loc=="<-"){
		loc = menu[previous_id].location; //Check previous id
	}else{
		previous_id = id; //Set previous id
	}
	console.log(loc);
	if(typeof(loc) === "undefined"){return false} //If no value
	if(!isdefault){ $("#humberger_btn").click(); }
	
	$.get("data/"+loc, function(data){
		html = marked(data);
	$('#page_ctn').showHtml(html,500,function(){
		var div = document.getElementById('page_ctn');
		Rainbow.color($("#page_ctn"));
	});
	},"text");

}
function f_filterResults(n_win, n_docel, n_body) {
	var n_result = n_win ? n_win : 0;
	if (n_docel && (!n_result || (n_result > n_docel)))
		n_result = n_docel;
	return n_body && (!n_result || (n_result > n_body)) ? n_body : n_result;
}

function f_scrollTop() {
	return f_filterResults (
		window.pageYOffset ? window.pageYOffset : 0,
		document.documentElement ? document.documentElement.scrollTop : 0,
		document.body ? document.body.scrollTop : 0
	);
}

$(window).load(function() {
  // When the page has loaded
  $("body").fadeIn(2000);
});


jQuery(function(){
	var kKeys = [];
	function Kpress(e){
		kKeys.push(e.keyCode);
		if (kKeys.toString().indexOf("38,38,40,40,37,39,37,39,73,83,78") >= 0) { //66,65 ba
			jQuery(this).unbind('keydown', Kpress);
			kExec();
		}
	}
	jQuery(document).keydown(Kpress);
});
function kExec(){
	$("body").append('<div id="eegs" style="background-color:red;display:none;"></div>');
	$("#site_place_holder").hide(0,function(){
		$('#eegs').css({
			width: $(document).width(),
			height: $(document).height(),
			opacity: 0.5
		});
		swfobject.embedSWF("http://img0.liveinternet.ru/images/attach/c/5//3970/3970473_sprite198.swf", "eegs", $(document).width()-5, $(document).height()-5, "9.0.0");
		$("#eegs").show();
		console.log("Done");
   });
}