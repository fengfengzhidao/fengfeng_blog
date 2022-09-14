axios.interceptors.request.use(request => {
    if (request.method !== 'get') {
        let csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value
        request.headers['X-CSRFToken'] = csrftoken
    }
    return request
})
axios.interceptors.response.use(response => {
    return response.data
})

/*
function dynamic_navigation() {
    let a_list = document.querySelectorAll('#dynamic_nav>a')
    let path = location.pathname
    for (const a of a_list) {
        let a_href = a.getAttribute('href')
        if (a_href === path || a_href + '/' === path) {
            a.classList.add('active')
        }
    }
}
dynamic_navigation()

 */
function getDisTop(element) {   //获取元素距离页面顶部的距离
    let realTop = element.offsetTop;
    let parent = element.offsetParent;
    while (parent !== null) {
        realTop += parent.offsetTop;
        parent = parent.offsetParent;
    }
    return realTop;
}

function setCookie(name, value) {
    let exp = new Date();
    exp.setTime(exp.getTime() + 2000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}

//获取cookie
function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");

    if (arr = document.cookie.match(reg))

        return unescape(arr[2]);
    else
        return null;
}

var vue = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],
    data: {
        // 弹窗宽度
        max_dialog_width: '50%',
        min_dialog_width: '30%',
        theme: 'light',  // 默认的主题
        this_category: 'qianduan', // 当前所在的位置
        comment_content: '', // 评论内容

        isShowSlider: false,
        slide_list: [],
        slide_text: '显示悬浮目录',

        nav_drawer: false,

        search_key: '',

        news_list: [],  // 新闻列表

        news_init: [
            {
                name: '微博',
                id: 'KqndgxeLl9',
                url: '/static/my/img/news/weibo.png'
            },
            {
                name: '知乎',
                id: 'mproPpoq6O',
                url: 'https://file.ipadown.com/tophub/assets/images/media/zhihu.com.png_50x50.png'
            },
            {
                name: '微信',
                id: 'WnBe01o371',
                url: 'https://file.ipadown.com/tophub/assets/images/media/mp.weixin.qq.com.png_50x50.png'
            },
            {
                name: '百度',
                id: 'Jb0vmloB1G',
                url: 'https://file.ipadown.com/tophub/assets/images/media/baidu.com.png_50x50.png'
            },
            {
                name: '36氪',
                id: 'Q1Vd5Ko85R',
                url: 'https://file.ipadown.com/tophub/assets/images/media/36kr.com.png_50x50.png'
            },
            {
                name: '哔哩哔哩',
                id: '74KvxwokxM',
                url: 'https://file.ipadown.com/tophub/assets/images/media/bilibili.com.png_50x50.png'
            },
            {
                name: '抖音',
                id: 'DpQvNABoNE',
                url: 'https://file.ipadown.com/tophub/assets/images/media/iesdouyin.com.png_50x50.png'
            },
            {
                name: '拼多多',
                id: 'ARe1QZ2e7n',
                url: 'https://file.ipadown.com/tophub/assets/images/media/p.pinduoduo.com.png_50x50.png'
            }
        ],
        news_active: '微博',
        news_active_url: 'https://file.ipadown.com/tophub/assets/images/media/s.weibo.com.png_50x50.png',

        mood_dialogVisible: false,

        mood_add: {
            name: '',
            avatar_id: null,
            content: '',
            drawing: '',
        },

        mood_show_drawing: [],

        mood_comment_dialogVisible: false,

        mood_add_comment: {
            name: '',
            content: '',
        },

        history_dialogVisible: false,
        history: {
            title: '',
            create_date: new Date(),
            content: '',
            drawing: '',
        },
        history_edit_add: false,  // 默认是添加, 编辑是nid
        history_show_drawing: [],
        history_pickerOptions: {
            disabledDate(time) {
                return time.getTime() > Date.now();
            }
        },
        site_title: {
            title: ''
        },
        site_dialogVisible: false,
        site_add_edit_tag: false,
        site_tab_tag: '推荐',
        site_list: [],
        site_add_dialogVisible: false,
        site: {
            title: '',
            abstract: '',
            href: '',
            icon_href: '',
            tag: [],
        },
        site_add_edit: false,
        site_order: 'create_date',

        friends_links_dialog: false,

        feedback: {
            email: '',
            content: '',
        },

        article_pwd: '',
        edit_cover_dialog: false,
        edit_cover: {
            nid: '',  // 图片id
            aid: '',  // 文章id
        },

        project_dialog: false,
        project: {
            title: '',
            article: [],
        },
        project_add_edit: false,

    },
    created() {

        this.init_dialog_width()

        this.init_theme()

        let path = location.pathname
        if (path.indexOf('article') !== -1 || path.indexOf('about') !== -1) {
            this.init_slider()
        }
        if (path.indexOf('search') !== -1) {
            this.init_search_key()
        }

        if (path.indexOf('news') !== -1) {
            this.news_init_method(0)
        }
        if (path === '/') {
            this.news_init_method(1)
        }
        if (path.indexOf('sites') !== -1) {
            this.init_site()
        }


        setTimeout(() => {
            this.get_sidebar()
            this.code_copy()
        }, 200)


    },
    mounted() {
        this.keyDown()
        let path = location.pathname
        if (path.indexOf('search') === -1) {
            setTimeout(() => {
                this.init_scrollbar()
            }, 100)

        }
    },
    methods: {
        // 初始化弹窗大小
        init_dialog_width() {
            let w = $(document).width()
            if (w > 850) {

            } else if (w > 550) {
                this.max_dialog_width = '70%'
                this.min_dialog_width = '50%'
            } else if (w > 400) {
                this.max_dialog_width = '90%'
                this.min_dialog_width = '70%'
            } else {
                this.max_dialog_width = '100%'
                this.min_dialog_width = '90%'
            }
        },

        // 初始化主题
        init_theme() {
            // 读取存储的主题信息
            let theme = localStorage.getItem('theme')
            if (theme) {
                this.theme = theme
            }
        },

        // 设置主题
        setTheme(themeName) {
            this.theme = themeName
            // 持久化存储
            localStorage.setItem('theme', themeName)
        },

        handleCommand(command) {
            location.href = command
        },

        nav_open() {
            $('nav, .my_header,main,footer').addClass('open')
        },

        nav_close() {
            $('nav, .my_header,main,footer').removeClass('open')
        },

        // 图片加载失败
        img_error(e) {
            e.target.style.display = 'none'
        },

        // 监听方向键
        keyDown() {
            // 监听键盘
            let el_bar = document.querySelector('.el-scrollbar__wrap')
            document.onkeydown = (e) => {
                //事件对象兼容
                let e1 = e || event || window.event || arguments.callee.caller.arguments[0]
                if (e1.target.classList.contains('viewer-open')) {
                    return
                }

                let top = el_bar.scrollTop  // 获取现在的位置
                if (e1.code === 'ArrowDown') {  // 下
                    $(el_bar).animate({scrollTop: top + 20}, 0)
                } else if (e1.code === 'ArrowUp') { // 上
                    $(el_bar).animate({scrollTop: top - 20}, 0)
                }
            }
        },

        // 滚动条初始化
        init_scrollbar() {
            let bar = this.$refs.scrollbar.wrap
            let slider = document.querySelector('.slide_or_actions')
            let nav = document.querySelector('.nav_bg')
            let top1 = 0;
            let path = location.pathname
            let old_url = localStorage.getItem('current_url')
            let new_url = location.href
            if (path.indexOf('article') !== -1 || path.indexOf('about') !== -1) {
                top1 = $(slider).offset().top - 80
            }
            if (old_url === new_url) {
                // 刷新
                let top = localStorage.getItem('current_top')
                localStorage.setItem('current_top', '0')
                let el_bar = document.querySelector('.el-scrollbar__wrap')
                $(el_bar).animate({scrollTop: top}, 0)
            }

            bar.onscroll = () => {
                let top = bar.scrollTop

                if (top >= 200) {
                    nav.classList.add('show')
                } else {
                    nav.classList.remove('show')
                }
                if (slider) {
                    if (top >= top1) {
                        slider.classList.add('fixed')
                    } else {
                        slider.classList.remove('fixed')
                    }
                }
            }
        },

        // 选择分类
        switch_article_category(categoryName) {
            this.this_category = categoryName
        },

        // 发布评论
        add_comment(nid) {
            let content = AnalyticMarkDown(this.comment_content)
            axios.post(`/api/article/${nid}/comment/`, {content}).then(res => {
                if (res.code) {
                    if (res.self) {
                        this.$refs[`comment_${res.self}`].focus();
                    }
                    this.$message.error(res.msg)
                    return
                }
                this.$message.success(res.msg)
                setTimeout(() => {
                    location.reload()
                }, 500)
            })
        },

        // 将被评论人的用户名写到placeholder
        set_sub_placeholder(div, username, cid) {
            $(div).find('textarea').attr('placeholder', `@${username}`)
            $(div).find('textarea')[0].focus()
            $(div).find('textarea').attr('cid', cid)

        },

        // 展示子评论列表
        show_sub_comment_list(e, username, cid) {
            let div = $(e.target).parent().parent().next()
            $(div).slideToggle()
            // div
            this.set_sub_placeholder(div, username, cid)


        },

        // 子评论回复显示
        sub_comment_set_placeholder(e, username, cid) {
            let div = $(e.target).parents('.sub_comment_list')
            this.set_sub_placeholder(div, username, cid)
        },

        // 发布子评论
        add_sub_comment(e, nid) {
            // nid 文章id
            // cid  评论id

            axios.post(`/api/article/comment/${nid}/`, {
                content: $(e.target).prev().val(),
                pid: $(e.target).prev().attr('cid')
            }).then(res => {
                if (res.code) {
                    if (res.self) {
                        this.$refs[`sub_comment_${res.self}`].focus();
                    }
                    this.$message.error(res.msg)
                    return
                }
                this.$message.success(res.msg)
                setTimeout(() => {
                    location.reload()
                }, 500)
            })
        },

        // 删除子评论
        delete_sub_comment(nid, aid, root_comment_id) {
            this.$confirm('此操作将永久删除该评论, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                axios.delete(`/api/article/comment/${nid}/`, {
                    data: {
                        aid,
                        pid: root_comment_id
                    }
                }).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        return
                    }
                    this.$message.success(res.msg)
                    setTimeout(() => {
                        location.reload()
                    }, 500)
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '取消删除'
                });
            });

        },

        // 评论点赞
        comment_digg(e, nid) {
            axios.post(`/api/comment/digg/${nid}/`).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    return
                }
                e.target.innerHTML = `点赞（${res.data}）`
                this.$message.success(res.msg)
            })
        },

        // 文章点赞
        article_digg(e, nid) {
            let dom = e.target
            dom.classList.add('show')
            axios.post(`/api/article/digg/${nid}/`).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    return
                }
                $(dom).next().text(res.data)
                this.$message.success(res.msg)
            })

            let timer = null

            timer = setTimeout(() => {
                clearTimeout(timer)
                dom.classList.remove('show')
            }, 1000)
        },

        // 文章收藏
        article_collects(e, nid) {
            let dom = e.target
            axios.post(`/api/article/collects/${nid}/`).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    return
                }
                this.$message.success(res.msg)
                $(dom).next().text(res.data)
                if (res.isCollects) {
                    dom.classList.add('show')
                    return
                }
                dom.classList.remove('show')
            })
        },

        // 回到顶部
        go_to_top() {
            let bar = this.$refs.scrollbar.wrap
            $(bar).animate({
                scrollTop: 0
            }, 500)
        },

        init_slider() {
            let flag = localStorage.getItem('isShowSlider')
            setTimeout(() => {
                let box = document.querySelectorAll('.el-scrollbar__view')[1]
                let height = box.offsetHeight
                if (height > 500) {
                    height = 500
                } else if (height === 0) {
                    height = 200
                }
                document.getElementById('el_scrollbar').style.height = height + 'px'
            }, 300)
            if (flag) {
                flag = eval(flag)
                this.isShowSlider = flag
                this.$nextTick(() => {
                    this.sliderChange(flag)
                })
            } else {
                this.isShowSlider = false
                this.$nextTick(() => {
                    this.sliderChange(false)
                })
            }
        },

        // 悬浮目录是否显示
        sliderChange(val) {
            /*
            let dom = this.$refs.slider

            localStorage.setItem('isShowSlider', val)
            if (val) {
                dom.classList.add('show')
                this.slide_text = '关闭悬浮目录'
                return
            }
            dom.classList.remove('show')
            this.slide_text = '显示悬浮目录'

             */
            let dom = this.$refs.slider
            localStorage.setItem('isShowSlider', val)
            if (val) {
                dom.classList.add('show')
                this.side_text = '关闭悬浮目录'
                $(dom).find('.body').slideDown()
                return
            }
            this.side_text = '开启悬浮目录'
            $(dom).find('.body').slideUp()
            dom.classList.remove('show')

        },

        // 悬浮目录
        get_sidebar() {
            let content = $('#article_content')
            let h_list = content.children('h1,h2,h3,h4')
            let lis = []
            for (let i = 0; i < h_list.length; i++) {
                let c = h_list[i].innerText
                let tagName = h_list[i].tagName
                let tagId = h_list[i].id
                let ele = {
                    tagName,
                    c,
                    pos: '#' + tagId
                }
                lis.push(ele)
            }

            lis.push({
                tagName: 'H1',
                c: '去评论吧！',
                pos: '.comment_submit'
            })
            this.slide_list = lis
        },
        //
        go_side_bar(selector, e) {
            $('.slider_bar .body p').css('color', '')
            let bar = this.$refs.scrollbar.wrap

            e.target.style.color = '#ff9800'
            let top = getDisTop($(selector)[0])
            $(bar).animate({scrollTop: top - 80}, 600)
        },

        // 代码一键复制
        code_copy() {
            $('pre').each(function () {
                let copy = $('<i title="copy" class="el-icon-document-copy code-copy"></i>')
                $(this).append(copy)
            })

            $('pre i.code-copy').click(e => {

                let text_list = $(e.target).prev().find('code')
                let text = ''
                text_list.each(function () {
                    text += $(this).text() + '\n'
                })
                let element = $('<textarea>' + text + '</textarea>')
                $('body').append(element)
                element[0].select()
                document.execCommand('Copy')
                element.remove()

                // 复制成功的提示信息
                this.$message.success('复制成功！')

            })

        },


        // 点击搜索
        search(path = '/search/', target = '_blank') {
            let box = document.querySelector('.search')

            if (!box.classList.contains('show_search')) {
                // 搜索框展开
                box.classList.add('show_search')
                // 需要给input添加焦点
                box.querySelector('input').focus()
                return
            }
            if (!this.search_key) {
                // 没有搜索词的时候点搜索按钮
                box.classList.remove('show_search')
                return;
            }
            // 打开标签页
            window.open(path + '?key=' + this.search_key, name = target)
        },

        // 初始化搜索词
        init_search_key() {
            let dom = document.querySelector('.search_key_input')
            let key = dom.getAttribute('data')
            this.search_key = key
        },

        // 获取热搜数据
        get_new_data(id, name, url, flag, size) {
            if (name === this.news_active && !flag) {
                return
            }
            this.news_active = name
            this.news_active_url = url

            let data = {
                id,
            }
            if (size) {
                data.size = size
            }

            let headers = this.news_headers

            axios.post('/api/news/', data, {headers}).then(res => {
                this.news_list = res.data
            })
        },

        // 初始化新闻，获取加密头
        news_init_method(size) {
            setTimeout(() => {
                let e = new Date;
                e.toUTCString();
                const t = e.getTime().toString();
                let signaturekey = $.OM.AES.encrypt(t, "itab1314").toString()
                this.news_headers = {
                    signaturekey,
                }
                this.get_new_data('KqndgxeLl9', '微博', '/static/my/img/news/weibo.png', true, size)
            }, 100)


        },

        mood_show_comment_list(e) {
            let div = $(e.target).parent().parent().next()
            div.slideToggle()
        },

        // 发布心情
        mood_add_method() {
            axios.post('/api/moods/', this.mood_add).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    this.$refs[`mood_add__${res.self}`].focus()
                    return
                }
                this.$message.success(res.msg)
                setTimeout(() => {
                    location.reload()
                }, 1000)

            })
        },

        // 删除心情
        mood_delete(nid, e) {
            this.$confirm('此操作将永久删除该心情, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                axios.delete(`/api/moods/${nid}/`).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        return
                    }
                    this.$message.success(res.msg)
                    setTimeout(() => {
                        $(e.target).parents('.mood').remove()
                    }, 500)
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },

        // 打开回复心情的对话框
        mood_comment_dialogVisible_show(nid) {
            this.mood_comment_dialogVisible = true
            this.mood_comment_add_method.nid = nid

        },

        // 心情评论
        mood_comment_add_method() {
            let nid = this.mood_comment_add_method.nid

            axios.post(`/api/mood_comments/${nid}/`, this.mood_add_comment).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    this.$refs[`mood_comment_add__${res.self}`].focus()
                    return
                }
                this.$message.success(res.msg)
                setTimeout(() => {
                    location.reload()
                }, 1000)
            })
        },


        // 心情评论删除
        mood_sub_comment_delete(nid, mood_id, e) {
            this.$confirm('此操作将永久删除该评论, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                // nid是评论id，mood_id是心情id
                axios.delete(`/api/mood_comments/${nid}/`, {
                    data: {
                        mood_id,
                    }
                }).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        return
                    }
                    this.$message.success(res.msg)
                    setTimeout(() => {
                        $(e.target).parents('.mood').find('.mood_comment_num').text(`评论（${res.data}）`)
                        $(e.target).parents('li').remove()
                    }, 300)
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },

        // 心情点赞和心情评论点赞
        mood_digg(path, nid, e) {
            axios.put(`/api/${path}/${nid}/`).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    return
                }
                this.$message.success(res.msg)
                $(e.target).text(`点赞（${res.data}）`)
            })
        },


        uploadImgFromPaste(file) {
            axios.post('/api/paste_upload/', {image: file}).then(res => {
                this.history.drawing += res.url + '\n'
            })
        },


        history_add_edit_method(nid) {
            axios.post('/api/history/' + nid, this.history).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    return
                }
                this.$message.success(res.msg)
                this.history_dialogVisible = false
                location.reload()
            })
        },

        history_add_method(nid) {
            if (!nid) {
                // 添加事件
                this.history_add_edit_method('')
                return
            }
            // 编辑事件
            this.history_add_edit_method(nid + '/')
        },

        paste_upload(e) {
            let clipboardData = (e.clipboardData || e.originalEvent.clipboardData);
            let items = clipboardData.items, len = items.length, blob = null;


            //在items里找粘贴的image,据上面分析,需要循环
            for (let i = 0; i < len; i++) {
                if (items[i].type.indexOf("image") !== -1) {
                    //getAsFile() 此方法只是living standard firefox ie11 并不支持
                    blob = items[i].getAsFile();
                }
            }
            if (blob !== null) {
                // 读取图片文件
                let reader = new FileReader();
                reader.onload = (event) => {
                    // event.target.result 即为图片的Base64编码字符串
                    let base64_str = event.target.result
                    //可以在这里写上传逻辑 直接将base64编码的字符串上传（可以尝试传入blob对象，看看后台程序能否解析）
                    this.uploadImgFromPaste(base64_str);
                }
                reader.readAsDataURL(blob);
                //阻止默认行为即不让剪贴板内容在div中显示出来
                // e.preventDefault();
            }

        },

        history_edit_show(e, nid, title, create_date) {
            this.history.title = title
            this.history.create_date = create_date
            let div = e.target
            this.history_edit_add = nid
            this.history.content = div.getAttribute('content')
            this.history.drawing = div.getAttribute('drawing')
            this.history_dialogVisible = true
        },

        history_remove(nid, e) {
            this.$confirm('此操作将永久删除该事件, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                // nid是评论id，mood_id是心情id
                axios.delete(`/api/history/${nid}/`).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        return
                    }
                    $(e.target).parents('.timeline-item').remove()
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },

        history_handleClose(done) {
            this.$confirm('关闭之后，修改的数据失效，确认关闭？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(() => {
                    this.history.title = ''
                    this.history.create_date = new Date()
                    this.history_edit_add = false
                    this.history.content = ''
                    this.history.drawing = ''
                    done();
                })
                .catch(() => {
                });
        },


        site_add_edit_tag_method(nid) {
            axios.post('/api/site_tag/' + nid, this.site_title).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    return
                }
                this.$message.success(res.msg)
                location.reload()
            })
        },

        site_add_tag(nid) {
            if (!nid) {
                // 添加事件
                this.site_add_edit_tag_method('')
                return
            }
            // 编辑事件
            this.site_add_edit_tag_method(nid + '/')
        },

        site_tag_edit_show(nid, title) {
            this.site_add_edit_tag = nid
            this.site_title.title = title
            this.site_dialogVisible = true
        },

        site_tag_handleClose(done) {
            this.site_add_edit_tag = false
            this.site_title.title = ''
            done()
        },

        site_tag_remove(e, nid) {
            this.$confirm('此操作将永久删除该标签, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                // nid是评论id，mood_id是心情id
                axios.delete(`/api/site_tag/${nid}/`).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        return
                    }
                    $(e.target).remove()
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },

        site_tag_tab_show(title) {
            this.site_tab_tag = title

            this.site_get_list(title, this.site_order)
        },

        site_get_list(title, order) {
            axios.get('/api/sites/', {
                params: {
                    title,
                    order,
                }
            }).then(res => {
                this.site_list = res

            })
        },

        init_site() {
            this.site_get_list(this.site_tab_tag, this.site_order)
        },

        site_add(nid) {
            if (!nid) {
                axios.post('/api/sites/', this.site).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        $(`#site_add__${res.self}`)[0].focus()
                        return
                    }
                    this.$message.success(res.msg)
                    this.site_add_dialogVisible = false
                    this.init_site()
                })
            } else {
                axios.put(`/api/sites/${nid}/`, this.site).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        $(`#site_add__${res.self}`)[0].focus()
                        return
                    }
                    this.$message.success(res.msg)
                    this.site_add_dialogVisible = false
                    this.init_site()
                })
            }

            this.site = {
                title: '',
                abstract: '',
                href: '',
                icon_href: '',
                tag: [],
            }

        },

        site_edit_show(item) {
            let tag = []
            for (const itemElement of item.tags) {
                tag.push(itemElement.nid)
            }
            this.site = {
                title: item.title,
                abstract: item.abstract,
                href: item.href,
                icon_href: item.icon_href,
                tag,
            }
            this.site_add_edit = item.nid
            this.site_add_dialogVisible = true
        },

        site_edit_close(done) {
            done()
            this.site_add_edit = false
            this.site = {
                title: '',
                abstract: '',
                href: '',
                icon_href: '',
                tag: [],
            }

        },

        site_remove(e, nid) {
            this.$confirm('此操作将永久删除该网站, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                // nid是评论id，mood_id是心情id
                axios.delete(`/api/sites/${nid}/`).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        return
                    }
                    $(e.target).parent().parent().remove()
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },

        site_order_method(order) {
            this.site_order = order
            this.site_get_list(this.site_tab_tag, this.site_order)
        },

        site_digg(e, item) {
            axios.post(`/api/site_digg/${item.nid}/`).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    return
                }
                this.$message.success(res.msg)
                item.digg_count += 1

                $(e.target).parent().addClass('show')

                setTimeout(() => {
                    $(e.target).parent().removeClass('show')
                }, 2000)
            })
        },

        site_coll(e, item) {
            axios.post(`/api/site_coll/${item.nid}/`).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    return
                }
                this.$message.success(res.msg)
                if (res.data === 1) {
                    $(e.target).parent().addClass('show')
                } else {
                    $(e.target).parent().removeClass('show')
                }
                item.collects_count += res.data

            })
        },

        friend_link_add() {
            axios.post('/api/friends_links/', this.site).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    $(`#site_add__${res.self}`)[0].focus()
                    return
                }
                this.$message.success(res.msg)
                this.friends_links_dialog = false
            })
        },

        feedback_add() {
            axios.post('/api/feedback/', this.feedback).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    $(`#feedback__${res.self}`)[0].focus()
                    return
                }
                this.$message.success(res.msg)
                this.feedback.content = ''
            })
        },

        article_pwd_show(nid) {
            axios.post(`/api/article_pwd/${nid}/`, {pwd: this.article_pwd}).then(res => {
                if (res.code) {
                    this.$message.error(res.msg)
                    document.getElementById('article_pwd').focus()
                    return
                }
                this.$message.success(res.msg)
                location.reload()

            })
        },

        show_edit_cover(aid, nid) {
            this.edit_cover.nid = nid
            this.edit_cover.aid = aid
            this.edit_cover_dialog = true
        },

        edit_cover_method(aid) {
            // aid 文章的id
            let nid = this.edit_cover.nid  // 新的图片id
            axios.post(`/api/article/cover/${aid}/`, {nid}).then(res => {
                location.reload()
            })
        },

        project_edit_show(lis, title, nid) {
            this.project.title = title
            this.project_add_edit = nid
            this.project.article = eval(lis)
            this.project_dialog = true
        },

        project_handleClose(done) {
            done()
            this.project_dialog = false
            this.project.title = ''
            this.project_add_edit = false
            this.project.article = []

        },

        project_add(nid) {
            if (nid) {
                axios.put(`/api/projects/${nid}/`, this.project).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        return
                    }
                    this.$message.success(res.msg)
                    setTimeout(() => {
                        location.reload()
                    }, 1000)

                })
            } else {
                axios.post('/api/projects/', this.project).then(res => {
                    if (res.code) {
                        this.$message.error(res.msg)
                        return
                    }
                    this.$message.success(res.msg)
                    setTimeout(() => {
                        location.reload()
                    }, 1000)
                })
            }
            this.project_add_edit = false

        }

    },
    watch: {
        'mood_add.drawing'(n, o) {
            this.mood_show_drawing = n.split('\n')
        },
        'history.drawing'(n, o) {
            this.history_show_drawing = n.split('\n')
        },

    }
})
let w = true;  // 点击a标签的跳转就回到顶部
$('a').click(e => {
    w = false
})
window.onbeforeunload = e => {
    // 将滚动条的位置和当前url写入
    if (w) {
        let el_bar = document.querySelector('.el-scrollbar__wrap')
        let url = location.href
        localStorage.setItem('current_top', el_bar.scrollTop)  // 离开前 距离页面顶部的高度
        localStorage.setItem('current_url', url)  // 离开前的的网站路径
    }


};

