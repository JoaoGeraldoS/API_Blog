from app.models import Categories, PostCategory, db, Tags, PostTags

def add_category(post_id, category, categories):
    
    if not categories:
        
        add_category = Categories(name = category)
        db.session.add(add_category)
        db.session.commit()

        print(add_category)
        add_post_category(id_post=post_id, category_id=add_category.id)
    else:
        print(category)
        add_post_category(id_post=post_id, category_id=categories)
        

def add_post_category(id_post, category_id):
    category_post = PostCategory(post_id = id_post, category_id=category_id)
    db.session.add(category_post)
    db.session.commit()


def add_tag(post_id, tag, tags):
    if not tags:
        add_tag = Tags(name = tag)
        db.session.add(add_tag)
        db.session.commit()

        add_tag_post(id_post=post_id, tag_id=add_tag.id)
    else:
        add_tag_post(id_post=post_id, tag_id=tags)


def add_tag_post(id_post, tag_id):
    tag_post = PostTags(post_id=id_post, tag_id = tag_id)
    db.session.add(tag_post)
    db.session.commit()
