/*鼠标移入事件，动态添加div*/
function mouseOver(event){
	$(event.target).children().css("display","inline-block");
	$(event.target).children().children().css({"border-bottom":"1px dashed orange",
	"margin":"5px","margin-top":"10px","line-height":"20px"});
}
/*为鼠标绑定移动事件*/
function mouseMove(event){
	var left=event.offsetX+20;
	var top=event.offsetY+20;
	$(event.target).children().css("top",top+"px");
	$(event.target).children().css("left",left+"px");
}
/*为鼠标绑定移除事件*/
function mouseOut(event){
	$(event.target).children().css("display","none");
}


<!--  点击购买出现效果 -->
function onClick(event){
	var $form=$("<form action='shop' method='post'></form>")
	/*整个购买框*/
	var $div0=$("<div></div>");
 	/*整个背景图片*/
	var $div1=$("<div></div>");
	/*购买道具*/
	var $div2=$("<div></div>");
	/*取消*/
	var $div3=$("<div></div>");
	/*确认*/
	var $div4=$("<button value='submit'></button>");
	var $hidden=$(event.target).children();
	$(event.target).append($form);
	$form.append($div0);
	$div0.append($hidden);
	$div0.append($div4);
	$div0.append($div3);
	$div0.append($div2);
	$div0.append($div1);
	$div1.text("确认购买该工具?");

	$div0.toggleClass("div0");
	$div1.toggleClass("div1");
	$div2.toggleClass("div2");
	$div3.toggleClass("div3");
	$div4.toggleClass("div4");
	/*阻止事件穿透*/
	$div0.click(function(event){
		event.stopPropagation();
	})
	/*点击事件*/
	$div3.click(function(){
		$div0.remove();
	})
	event.stopPropagation();
}




