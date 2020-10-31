$(function () {
    $('#get_employee').click(function () {
        $.get('/get_employee', function (data) {
            $("#employee").empty()
                .append("<li>姓名："+ data.name+" </li>")
                .append("<li>年龄："+ data.age +" </li>")
                .append("<li>性别："+ data.sex +" </li>")
                .append("<li>工资："+ data.salary +" </li>")
                .append("<li>备注信息："+ data.comment +" </li>");
        })
    })
})


$(function () {
    $('#province').change(function () {
        var area_id = $(this).val();    // 选中的省份id

        $('#city').empty().append('<option>--请选择城市--</option>');
        $('#district').empty().append('<option>--请选择区县--</option>');

        // 发起ajax get请求,获取城市数据并显示
        $.get('/get_children/' + area_id, function (data) {
            // data: 服务器返回的城市数据
            var areas = data.children;
            // each: 遍历数组
            $.each(areas, function (index, area) {// index: 第几次循环
                var id = area[0];        // 区域id
                var title = area[1];     // 区域名称
                $('#city')
                    .append('<option value="' + id + '">' + title + '</option>');
            });
        })
    });
})


$(function () {
    $('#city').change(function () {
        var area_id = $(this).val();
        $('#district').empty().append('<option>--请选择区县--</option>');

        // 发起ajax get请求,获取城市数据并显示
        $.get('/get_children/' + area_id, function (data) {
            // data: 服务器返回的城市数据
            var areas = data.children;
            // each: 遍历数组
            $.each(areas, function (index, area) {
                var id = area[0];
                var title = area[1];
                $('#district')
                    .append('<option value="' + id + '">' + title + '</option>');
            });
        })
    });
})