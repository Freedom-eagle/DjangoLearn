from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry


# Register your models here.
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):
		fields = ('title', 'desc')
		extra = 1
		model = Post


# 实际admin控制
@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
		inlines = [PostInline,]
		list_display = ('name', 'status', 'is_nav', 'created_time', 'owner')
		list_filter = []
		fields = ('name', 'status', 'is_nav')

		def post_count(self, obj):
				return obj.poost_set.count()
		post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
		list_display = ('name', 'status', 'created_time')
		fields = ('name', 'status')



# ----------自定义过滤器---------
class CategoryOwnerFilter(admin.SimpleListFilter):
		title = '分类'
		parameter_name = 'owner_category'

		def lookups(self, request, model_admin):
				return Category.objects.filter(owner=request.user).values_list('id', 'name')

		def queryset(self, request, queryset):
				category_id = self.value()
				if category_id:
						return queryset.filter(category_id=category_id)
				return queryset

@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
		exclude = ('owner',)
		form = PostAdminForm

		list_display = [
						'title', 'category', 'status',
						'created_time', 'owner', 'operator'
						]
		list_display_links = []
		list_filter = [CategoryOwnerFilter, ]
		search_fields = ['title', 'category__name']

		actions_on_top = True
		actions_on_buttom = True

		save_on_top = True

		fieldsets = (
						('基础配置', {
								'description': '基础配置描述',
								'fields': (
										('title', 'category'),
										'status',
										),
								}),
						('内容', {
								'fields': (
										'desc',
										'content',
										),
								}),
						('额外信息', {
								'classes': ('collapse'),
								'fields': ('tag', ),
								})
						)


		# filter_vertical = ('tag',)	
		filter_horizontal = ('tag',)

		def operator(self, obj):
				return format_html(
								'<a href="{}">编辑</a>',
								reverse('cus_admin:blog_post_change', args=(obj.id,))
								)
		operator.short_description = '操作'

		class Media:
				css = {
								'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrapmin.css", ),
								}
				js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
		list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
