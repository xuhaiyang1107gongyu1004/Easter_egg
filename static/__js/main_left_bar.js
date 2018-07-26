/**
 * Created by huchao on 2018/6/17.
 * 用来处理left_bar 的鼠标点击事件
 */

// window.onload = function () {
//     document.body.innerHTML = '<script src="jquery-3.3.1.js"><\/script>' + document.body.innerHTML;
// };
HOST = 'http://127.0.0.1:5000';

function leftBarClickSrc(btn) {
    btn.setAttribute("class", "btnHover");
    console.log(btn);
    switch (btn.id) {
        case "kymj":
        case "kymj_torbar_DZ":
        case "kymj_torbar_shop":
            // 矿源秘境
            location.href = "/KS";
            break;
        //    有上角 锻造大厅按钮
        case "dzdt_torbar_KS":
        case "dzdt_torbar_shop":
        case "dzdt":
            //在原有窗口打开页面
            location.href = "/DZ";
            break;
        case "smbox":
            // alert("打开神秘宝箱界面");
            location.href = "/box";
            break;
        case "sendhome":
            // alert("打开交易界面");
            location.href = "/send";
            break;
        case "bang":
            alert("程序员小哥哥小姐姐正在努力开发中，不要着急嘛！好不好！");
            alert("好不好嘛！！！");
            break;
        case "pmhome":
            alert("程序员小哥哥小姐姐正在努力开发中，不要着急嘛！好不好！");
            alert("好不好嘛！！！");
            break;
        case "shop":
        case 'shop_torbar_KS':
        case 'shop_torbar_DZ':
            location.href = "/shop"
    }
}

function hiddenself(event) {
    $(event.target).remove()
}

function getData(URL, DATA) {

    $.ajax({
        //提交数据的类型 POST GET
        type: "POST",
        //提交的网址
        url: URL,
        //提交的数据
        data: DATA,
        //返回数据的格式
        datatype: "json",//"html",//"xml", "html", "script", "json", "jsonp", "text".
        //在请求之前调用的函数
        beforeSend: function () {
            $("#msg").html("logining");
        },
        //成功返回之后调用的函数
        success: function (data) {
            $("#msg").html(decodeURI(data));
        },
        //调用执行后调用的函数
        complete: function (XMLHttpRequest, textStatus) {
            alert(XMLHttpRequest.responseText);
            alert(textStatus);
            //HideLoading();
        },
        //调用出错执行的函数
        error: function () {
            //请求出错处理
        }
    })
}