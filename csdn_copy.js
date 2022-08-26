// ==UserScript==
// @name         CSDN免登录复制
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://blog.csdn.net/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=csdn.net
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // Your code here...

    /**
     * csdn的文章编写分为两种模式：
     *  1. 富文本
     *  2. markdown
     */


    //markdown模式下的“登录后复制”按钮失效
    document.querySelectorAll('code').forEach(x => {
        x.removeAttribute('onclick');
    })


    document.querySelectorAll('.signin').forEach(x => {
        x.removeAttribute('onclick'); //富文本模式下的“登录后复制”按钮失效
        x.setAttribute('data-title', 'copy');
        x.addEventListener('click', function () {
            let content = x.parentNode.innerText;
            // copy(content);  //document.execCommand已不推荐使用，此方法丢弃

            navigator.clipboard.writeText(content).then(() => {
                //复制成功
                console.log("copy success");
            },() => {
                //复制失败
                alert("copy failed");
            })

            x.setAttribute('data-title', 'copy success');
            setTimeout(function () {
                x.setAttribute('data-title', 'copy');
            }, 400);
        })
    })



    // 通过创建一个临时的文本域实现内容复制，且每次用完后删除
    // function copy(content) {
    //     let area = document.createElement('TextArea');
    //     document.body.appendChild(area);
    //     area.value = content;
    //     area.select();

    //     if (document.execCommand('copy')) {
    //         document.execCommand('copy');
    //     }

    //     document.body.removeChild(area);
    // }
})();