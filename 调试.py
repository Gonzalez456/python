from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

  arr = []
     file = open(r'D:\tag.txt','r')
     data = file.read().split('\r\n')
     for content in data:
         contents = validatecontent(content).split()
         for word in contents:
             arr.append(word)

tags = make_tags(get_tag_counts(YOUR_TEXT), maxsize=120)

create_tag_image(tags, 'cloud_large.png', size=(900, 600), fontname='Lobster')


# def main():
#     finance_cloud()
#
#
# if __name__ == '__main__':
#     main()