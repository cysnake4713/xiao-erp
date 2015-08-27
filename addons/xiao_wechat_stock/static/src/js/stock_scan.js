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

    $('.check_state').on('click', function (e) {
        e.preventDefault();
        var loading = $.loading({
            content: '加载中...'
        });
        //window.location.href = new URI(window.location.href).setSearch('update_state', '1')
        $.post('/mobile/stock/scan/update', {
                'id': $('.data_form').first().data('id'),
                'update_state': 1
            },
            function () {
                //loading.loading("hide");
                location.reload();
            }
        );
    });

    $('.update_carrier_ref').on('click', function (e) {
        e.preventDefault();
        var loading = $.loading({
            content: '加载中...'
        });
        //window.location.href = new URI(window.location.href).setSearch('update_carrier_ref',$('.carrier_tracking_ref').val() );
        $.post('/mobile/stock/scan/update', {
                'id': $('.data_form').first().data('id'),
                'update_carrier_ref': $('.carrier_tracking_ref').val()
            },
            function () {
                location.reload();
            }
        );
    });

    $('.transfer_all').on('click', function (e) {
        e.preventDefault();
        var loading = $.loading({
            content: '加载中...'
        });
        $.post('/mobile/stock/scan/update', {
                'id': $('.data_form').first().data('id'),
                'transfer_all': 1
            },
            function () {
                location.reload();
            }
        );
    });

    $('.carrier_tracking_ref_clear').on('click', function (e) {
        e.preventDefault();
        $('.carrier_tracking_ref').val('');
    });


});

