function getjq(yyyy, mm, dd) {

    mm = mm - 1;

    let sTermInfo = new Array(0, 21208, 42467, 63836, 85337, 107014, 128867, 150921, 173149, 195551, 218072, 240693, 263343, 285989, 308563, 331033, 353350, 375494, 397447, 419210, 440795, 462224, 483532, 504758);

    let solarTerm = new Array("小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至");

    let solarTerms = "";

    while (solarTerms === "") {
        let tmp1 = new Date((31556925974.7 * (yyyy - 1900) + sTermInfo[mm * 2 + 1] * 60000) + Date.UTC(1900, 0, 6, 2, 5));
        let tmp2 = tmp1.getUTCDate();
        if (tmp2 === dd) solarTerms = solarTerm[mm * 2 + 1];
        tmp1 = new Date((31556925974.7 * (yyyy - 1900) + sTermInfo[mm * 2] * 60000) + Date.UTC(1900, 0, 6, 2, 5));
        tmp2 = tmp1.getUTCDate();
        if (tmp2 === dd) solarTerms = solarTerm[mm * 2];
        if (dd > 1) {
            dd = dd - 1;
        } else {
            mm = mm - 1;
            if (mm < 0) {
                yyyy = yyyy - 1;
                mm = 11;
            }
            dd = 31;
        }
    }
    return solarTerms;
}

function set_jieqi_image() {
    let today = new Date();
    year = today.getFullYear()
    month = today.getMonth() + 1; //获取当前月份(0-11,0代表1月)
    day = today.getDate(); //获取当前日(1-31)

    let hourse_img = {
        '立春': ['0.png', '立春', 'translate(0px, -223px)'],
        '雨水': ['1.png', '雨水', 'translate(0px, -207px)'],
        '惊蛰': ['2.png', '惊蛰', 'translate(0px, -223px)'],
        '春分': ['3.png', '春分', 'translate(0px, -190px)'],
        '清明': ['4.png', '清明', 'translate(0px, -279px)'],
        '谷雨': ['5.png', '谷雨', 'translate(0px, -239px)'],
        '立夏': ['6.png', '立夏', 'translate(0px, -210px)'],
        '小满': ['7.png', '小满', 'translate(0px, -226px)'],
        '芒种': ['8.png', '芒种', 'translate(0px, -199px)'],
        '夏至': ['9.png', '夏至', 'translate(0px, -120px)'],
        '小暑': ['10.png', '小暑', 'translate(0px, -232px)'],
        '大暑': ['11.png', '大暑', 'translate(0px, -117px)'],
        '立秋': ['12.png', '立秋', 'translate(0px, -151px)'],
        '处暑': ['13.png', '处暑', 'translate(0px, -161px)'],
        '白露': ['14.png', '白露', 'translate(0px, -57px)'],
        '秋分': ['15.png', '秋分', 'translate(0px, -129px)'],
        '寒露': ['16.png', '寒露', 'translate(0px, -185px)'],
        '霜降': ['17.png', '霜降', 'translate(0px, -181px)'],
        '立冬': ['18.png', '立冬', 'translate(0px, -181px)'],
        '小雪': ['19.png', '小雪', 'translate(0px, -181px)'],
        '大雪': ['20.png', '大雪', 'translate(0px, -82px)'],
        '冬至': ['21.png', '冬至', 'translate(0px, -242px)'],
        '小寒': ['22.png', '小寒', 'translate(0px, -48px)'],
        '大寒': ['23.png', '大寒', 'translate(0px, -114px)'],
    }

    now = getjq(year, month, day)
    let load = hourse_img[now]
    if (load) {
        $('#jieqiset').attr('src', `/static/my/img/24_hourse/${load[0]}`).css('transform', `${load[2]}`).attr('title', load[1])
    }
}

set_jieqi_image()
// console.log(getjq(2022, 2, 19))