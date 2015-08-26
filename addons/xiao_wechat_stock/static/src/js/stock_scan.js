$(function () {
    $('.return-list').on('click', function (e) {
        e.preventDefault();
        window.location.href = this.children[0].href;
    });

    $('.scan-wechat').on('click', function (e) {
        wx.scanQRCode({
            desc: 'scanQRCode desc',
            needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
            scanType: ["qrCode", "barCode"], // 可以指定扫二维码还是一维码，默认二者都有
            success: function (res) {
                $('.carrier_tracking_ref').val(res.resultStr);
            }
        });
    });

    $('.carrier_tracking_ref_clear').on('click', function (e) {
        e.preventDefault();
         $('.carrier_tracking_ref').val('');
    });


});

