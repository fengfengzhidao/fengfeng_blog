from app01.models import Comment


def find_root_sub_comment(root_comment, sub_comment_list):
    for sub_comment in root_comment.comment_set.all():
        # 找根评论的子评论
        sub_comment_list.append(sub_comment)
        find_root_sub_comment(sub_comment, sub_comment_list)


def sub_comment_list(nid):
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
