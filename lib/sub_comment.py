from page.models import Comment


def find_root_sub_comment(root_comment, sub_comment_list):
    """
    获取某个根评论下的所有子评论
    root_comment：根评论对象
    sub_comment_list：将子评论放入的列表
    """
    for sub_comment in root_comment.comment_set.all():
        # 找根评论的子评论
        sub_comment_list.append(sub_comment)
        find_root_sub_comment(sub_comment, sub_comment_list)


def sub_comment_list(nid):
    """
    获取某个文章下的所有评论
    nid：文章id
    """
    # 找到某个文章的所有评论
    comment_query = Comment.objects.filter(article_id=nid).order_by('-create_time')
    # 把评论存储到列表
    comment_list = []

    for comment in comment_query:
        # 如果它的父亲是None，就说明是根评论
        if not comment.parent_comment:
            # 递归查找这个根评论下面的所有子评论
            lis = []
            find_root_sub_comment(comment, lis)
            comment.sub_comment = lis
            comment_list.append(comment)
            continue

    return comment_list


def find_root_comment(comment):
    """
    查找评论的根评论
    comment：评论对象
    """
    # 找comment的最终根评论
    if comment.parent_comment:
        # 还不是根评论
        # 递归去找它的根评论
        return find_root_comment(comment.parent_comment)
    # 是根评论，就返回出去
    return comment