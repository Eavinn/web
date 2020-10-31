window.onload = function () {
    
    // 1.获取两个按钮
    var oRed = document.getElementById('redInput');
    var oGreen = document.getElementById('greenInput');
    var oBody = document.getElementById('obody');
                
    // 2.监听点击事件 onclick
    oRed.onclick = function () {fnColorMethod("red")};

    oGreen.onclick = function () {fnColorMethod("green")};

    // 抽取 封装
    function fnColorMethod(bgcolor){
        oBody.style.backgroundColor = bgcolor;
        
    }
}


// window.onload = function () {
//     // splice 从开始位置，删除指定个数，增加的内容
//     var aArray = ['a', 'b', 'c'];
//     aArray.splice(1, 1, "**");
//     alert(aArray)
//     var sOne = "123867";
//     var aNewArray = sOne.split("");
//     var aSecondArray = aNewArray.reverse();
//     var sNewStr = aSecondArray.join("");
//     console.log(sNewStr)
// }

// window.onload = function () {
//     function fnAlert () {
//         alert('只执行一次')
//     }
//     setTimeout(fnAlert, 5000)
// }


