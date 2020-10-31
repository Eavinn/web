// window.onload = function () {
//     var oOne = document.getElementById("one");
//     var sColor = oOne.style.color
//     alert(sColor)
// }

// $(document).ready(function () {
//     var $div = $("#one");
//     var sColor = $div.css('color');
//     alert(sColor)
// })

$(function () {
    var $btns = $(".tap_btns input")
    var $div = $(".tab_cons").children()

    $btns.click(function () {
        $(this).addClass('active').siblings().removeClass("active");
        $div.eq($(this).index()).addClass('current').siblings().removeClass('current');

        // animate 样式属性，动画时长，动画状态，动画结束的时候执行函数
        $("#one").animate({"width":"500px","height":"300px","background-color":"red"}, 1000, "swing", function () {
           alert("hello world") 
        })
    })
})


$(document).ready(function () {
    console.log($('#one').prop('name'));
    $('#one').prop({'value':'用户名'})
    console.log($('#one').val())
    console.log($('#one').attr('renminbi'))
})


$(function() {
    $('#talksub').click(function () {
        var $sValue = $('#talkwords').val()
        if ($sValue == "") {
            alert('请输入文字！');
            return;}
        
        var $sOldContent = $('#words').html();
        var $sNewContent = '';
        if ($('#who').val() == '0') {
            $sNewContent = $sOldContent + '<div class="atalk"><span>A说:' + $sValue + '</span></div>' }
        else {
            $sNewContent = $sOldContent + '<div class="btalk"><span>B说:' + $sValue + '</span></div>' 
        }
        $('#words').html($sNewContent)
        $('#talkwords').val("")
    })
})

$(function () {
    var $lis = $('.li_list li');
    // for (var index = 0; index < $lis.length; index++) {
    //     $lis.eq(index).html(index)
    // each循环遍历的使用
    $lis.each(function (a, b) {
        // a是index, b是原生js标签对象
        console.log(b)
        $(b).html(a)
    
    // 委托事件
    $('.li_list').delegate('li', 'click', function() {$(this).css({'color':'red'})})
    })
})