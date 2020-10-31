// 设置和存储变量
var w, container, carousel, item, radius, itemLength, rY, ticker, fps; 
var mouseX = 0;
var mouseY = 0;
var mouseZ = 0;
var addX = 0;

// 定义了一个fps_counter对象
var fps_counter = {
	
	tick: function () 
	{
		// concat() 方法用于连接两个或多个数组,不断把当前时间加进数组中。
		this.times = this.times.concat(+new Date());
		var seconds, times = this.times;

		if (times.length > this.span + 1) 
		{
			// shift() 方法用于把数组的第一个元素从其中删除，并返回第一个元素的值
			times.shift(); 
			// 最后一个减去第一个的时间，然后除以1000，赋值给secondes
			seconds = (times[times.length - 1] - times[0]) / 1000;
			// Math.round() 方法可把一个数字舍入为最接近的整数。
			return Math.round(this.span / seconds);
		} 
		else return null;
	},
	// times数组
	times: [],
	// 长度比较
	span: 20
};
// 创建一个新对象
var counter = Object.create(fps_counter);


// 窗口加载等价于window.onload
$(document).ready( init )


function init()
{
	// 窗口
	w = $(window);
	// 最外层div
	container = $( '#contentContainer' );
	// section
	carousel = $( '#carouselContainer' );
	// figure
	item = $( '.carouselItem' );
	// figure的数量
	itemLength = $( '.carouselItem' ).length;

	fps = $('#fps');
	// 圆是360度除以figure数量，得到每一个的figure角度值
	rY = 360 / itemLength;
	// tan方法可返回一个表示某个角的正切的数字
	radius = Math.round( (250) / Math.tan( Math.PI / itemLength ) );
	
	// 设置container 3d 属性
	TweenMax.set(container, {perspective:600})
	TweenMax.set(carousel, {z:-(radius)})
	
	
	// 创建carousel item 属性
	for ( var i = 0; i < itemLength; i++ )
	{
		var $item = item.eq(i);
		// 找到背景图的div元素
		var $block = $item.find('.carouselItemInner');
		// 设置container 3d 属性
		TweenMax.set($item, {rotationY:rY * i, z:radius, transformOrigin:"50% 50% " + -radius + "px"});
		// 调用自己写的方法
		animateIn( $item, $block )						
	}
	
	// 设置 mouse x、y 属性 和 looper函数的ticker
	// 监听鼠标移动事件，onMouseMove方法记录值
	window.addEventListener( "mousemove", onMouseMove, false );
	// 设置无限执行的定时器
	ticker = setInterval( looper, 1000/60 );			
}

function animateIn( $item, $block )
{
	var $nrX = 360 * getRandomInt(2);
	var $nrY = 360 * getRandomInt(2);
		
	var $nx = -(2000) + getRandomInt( 4000 )
	var $ny = -(2000) + getRandomInt( 4000 )
	var $nz = -4
	000 +  getRandomInt( 4000 )
		
	var $s = 1.5 + (getRandomInt( 10 ) * .1)
	var $d = 1 - (getRandomInt( 8 ) * .1)
	
	TweenMax.set( $item, { autoAlpha:1, delay:$d } )	
	TweenMax.set( $block, { z:$nz, rotationY:$nrY, rotationX:$nrX, x:$nx, y:$ny, autoAlpha:0} )
	TweenMax.to( $block, $s, { delay:$d, rotationY:0, rotationX:0, z:0,  ease:Expo.easeInOut} )
	TweenMax.to( $block, $s-.5, { delay:$d, x:0, y:0, autoAlpha:1, ease:Expo.easeInOut} )
}

function onMouseMove(event)
{
	mouseX = -(-(window.innerWidth * .5) + event.pageX) * .0025;
	mouseY = -(-(window.innerHeight * .5) + event.pageY - 350) * .01;
	mouseZ = -(radius) - (Math.abs(-(window.innerHeight * .5) + event.pageY - 350) - 250);
}

// 循环和设置 3D属性
function looper()
{
	addX += mouseX
	TweenMax.to( carousel, 1, { rotationY:addX, rotationX:mouseY, ease:Quint.easeOut } )
	TweenMax.set( carousel, {z:mouseZ } )
	fps.text( 'Framerate: ' + counter.tick() + '/60 FPS' )	
}

function getRandomInt( $n )
{
	return Math.floor((Math.random()*$n)+1);	
}


// 旋转图形添加点击事件
$(function() {
	$("#contentContainer").delegate('.carouselItemInner', 'click', function(){
	var $imgUrl = $(this).css("backgroundImage"); 

	$("#big_pic").css({content:$imgUrl, height:0});
	var $urlAddress = $imgUrl.slice(5,-2)
	console.log($urlAddress)
	
	$("#big_pic").parent().attr('href', $urlAddress)
	$("#big_pic").animate({"width":"auto","height":"600px"}, 500,'swing');
	})

	var $lis = $('#top_list li');
	$lis.click(function () {
		$(this).animate({"left": 20 * $(this).index()});
		$(this).prevAll().each(function () {$(this).animate({"left": 20 * $(this).index()})});
		$(this).nextAll().each(function () {$(this).animate({"left": 350 - 20*($lis.length - $(this).index())})});
	
	})


});






		