# Generated by Django 5.1.2 on 2024-10-21 14:15

import django.db.models.deletion
import django_ckeditor_5.fields
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attribute', '0001_initial'),
        ('base_account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='O', unique=True, verbose_name='Mã đơn hàng')),
                ('total_payment', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tổng tiền')),
                ('payment_method', models.CharField(choices=[('online', 'Thanh toán trực tuyến'), ('cash', 'Thanh toán khi nhận hàng')], max_length=6, verbose_name='Phương thức thanh toán')),
                ('status', models.CharField(choices=[('pending', 'Đang chờ'), ('preparing', 'Đang chuẩn bị'), ('shipped', 'Đã vận chuyển'), ('deliverd', 'Đã nhận'), ('cannceled', 'Đã huỷ đơn')], default='pending', max_length=9, verbose_name='Trạng thái')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base_account.useraddress', verbose_name='Địa chỉ giao hàng')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng')),
            ],
            options={
                'verbose_name': 'Đơn Hàng',
                'verbose_name_plural': 'Đơn Hàng',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='S', unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='Tên giày')),
                ('image', models.ImageField(default='default/noimage.jpg', upload_to='images/shoes/', verbose_name='Ảnh')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Mô tả')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoes', to='attribute.brand', verbose_name='Thương hiệu')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoes', to='attribute.category', verbose_name='Danh mục')),
                ('tags', models.ManyToManyField(blank=True, related_name='shoes', to='attribute.tag', verbose_name='Thẻ')),
            ],
            options={
                'verbose_name': 'Giày',
                'verbose_name_plural': 'Giày',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(verbose_name='Bình luận')),
                ('rating', models.IntegerField(choices=[(1, '1 sao'), (2, '2 sao'), (3, '3 sao'), (4, '4 sao'), (5, '5 sao')], default=5, verbose_name='Đánh giá')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng')),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.shoe', verbose_name='Giày')),
            ],
            options={
                'verbose_name': 'Đánh giá',
                'verbose_name_plural': 'Đánh giá',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ShoeOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='SO', unique=True)),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Giá cũ')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Giá')),
                ('quantity', models.PositiveIntegerField(verbose_name='Số lượng')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='attribute.color', verbose_name='Màu sắc')),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='core.shoe', verbose_name='Giày')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='attribute.size', verbose_name='Kích cỡ')),
            ],
            options={
                'verbose_name': 'Chi tiết giày',
                'verbose_name_plural': 'Chi tiết giày',
            },
        ),
        migrations.CreateModel(
            name='ShoeOptionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default/noimage.jpg', upload_to='images/shoes/', verbose_name='Ảnh')),
                ('shoe_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.shoeoption')),
            ],
            options={
                'verbose_name': 'Ảnh',
                'verbose_name_plural': 'Ảnh',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='SC', unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng')),
            ],
            options={
                'verbose_name': 'Giỏ hàng',
                'verbose_name_plural': 'Giỏ hàng',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='SC', unique=True)),
                ('quantity', models.PositiveIntegerField(verbose_name='Số lượng')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.order', verbose_name='Đơn Hàng')),
                ('shoe_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.shoeoption', verbose_name='Chi tiết sản phẩm')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.shoppingcart', verbose_name='Giỏ Hàng')),
            ],
            options={
                'verbose_name': 'Mục hàng',
                'verbose_name_plural': 'Mục hàng',
            },
        ),
    ]
