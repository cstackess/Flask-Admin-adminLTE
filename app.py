# -*- coding: utf-8 -*-
from gettext import gettext

from flask import Flask, flash
from flask_admin import Admin
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
db = SQLAlchemy(app)


class Slice(db.Model):
    __tablename__ = 'tb_slice'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), unique=True, nullable=False)

    def import_slice(self):
        print("import")
        return True


class SliceView(ModelView):
    # 指定模板
    list_template = 'AdminLTE/list.html'
    create_template = 'AdminLTE/create.html'
    edit_template = 'AdminLTE/edit.html'
    details_template = 'AdminLTE/details.html'

    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'name': '名称'
    }
    column_searchable_list = ['name']
    column_filters = ['name']
    can_view_details = True
    can_export = True
    export_types = ['csv', 'xls', 'json', 'html']
    can_set_page_size = True

    @action('import', '导入', '是否导入数据？')
    def action_import(self, ids):
        try:
            count = 0
            query = Slice.query.filter(Slice.id.in_(ids))
            for s in query.all():
                result = s.import_slice()
                if not result:
                    raise Exception('Empty data')
                else:
                    count += 1
            flash('数据源成功导入！')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed to import slices. %(error)s', error=str(ex)), 'error')


admin = Admin(app=app, name='adminLTE', template_mode='bootstrap3', base_template='AdminLTE/mylayout.html', )  # 指定模板
admin.add_view(SliceView(Slice, db.session, name='数源管理', menu_icon_type='fa', menu_icon_value='fa-table'))
admin.add_link(MenuLink(name='模型图谱', url='#', icon_type='fa', icon_value='fa-sitemap'))
babel = Babel(app)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000)
