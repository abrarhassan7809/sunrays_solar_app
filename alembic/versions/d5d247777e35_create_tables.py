"""create tables

Revision ID: d5d247777e35
Revises: 
Create Date: 2023-08-26 18:29:35.190899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5d247777e35'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('joined', sa.DateTime(timezone=True), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('user_type', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('ac_cable',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('typ', sa.String(length=255), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Float(), nullable=True),
    sa.Column('sell_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('accessories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('typ', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Float(), nullable=True),
    sa.Column('sell_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('banks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=255), nullable=False),
    sa.Column('account_number', sa.String(length=255), nullable=False),
    sa.Column('bank_name', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('transaction_date', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account_number')
    )
    op.create_table('battery',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('typ', sa.String(length=255), nullable=True),
    sa.Column('warranty', sa.String(length=255), nullable=True),
    sa.Column('capacity', sa.String(length=255), nullable=True),
    sa.Column('voltage', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Float(), nullable=True),
    sa.Column('sell_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(length=255), nullable=True),
    sa.Column('company', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dc_cable',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('typ', sa.String(length=255), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Float(), nullable=True),
    sa.Column('sell_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expanse',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('frame',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('typ', sa.String(length=255), nullable=True),
    sa.Column('width', sa.String(length=255), nullable=True),
    sa.Column('height', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Float(), nullable=True),
    sa.Column('sell_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inverter',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('typ', sa.String(length=255), nullable=True),
    sa.Column('power_rating', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Float(), nullable=True),
    sa.Column('sell_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('labor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('labor_name', sa.String(length=255), nullable=False),
    sa.Column('start_date', sa.String(), nullable=True),
    sa.Column('phon_number', sa.String(length=255), nullable=True),
    sa.Column('labor_cnic', sa.String(length=255), nullable=True),
    sa.Column('labor_address', sa.String(length=255), nullable=True),
    sa.Column('labor_pay', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('panel',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('typ', sa.String(length=255), nullable=True),
    sa.Column('capacity', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchase_price', sa.Float(), nullable=True),
    sa.Column('sell_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_code', sa.String(length=255), nullable=False),
    sa.Column('project_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('project_cost', sa.Integer(), nullable=True),
    sa.Column('receiving_amount', sa.Integer(), nullable=True),
    sa.Column('remaining_amount', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quotation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('invoice_code', sa.String(), nullable=True),
    sa.Column('customer_name', sa.String(), nullable=True),
    sa.Column('walk_in_customer', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('grand_total', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('receiving_amount', sa.Float(), nullable=True),
    sa.Column('remaining_amount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supplier',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('supplier_name', sa.String(length=255), nullable=False),
    sa.Column('company', sa.String(length=255), nullable=False),
    sa.Column('phon_number', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bank_transaction',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('bank_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=255), nullable=False),
    sa.Column('account_number', sa.String(length=255), nullable=False),
    sa.Column('bank_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('transaction_date', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('labor_paid',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('labor_id', sa.Integer(), nullable=False),
    sa.Column('labor_name', sa.String(length=255), nullable=False),
    sa.Column('labor_cnic', sa.String(length=255), nullable=True),
    sa.Column('absent_days', sa.Integer(), nullable=True),
    sa.Column('present_days', sa.Integer(), nullable=True),
    sa.Column('remaining_pay', sa.Float(), nullable=True),
    sa.Column('last_paid', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['labor_id'], ['labor.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quotation_item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('quotation_id', sa.Integer(), nullable=False),
    sa.Column('product_code', sa.String(length=255), nullable=True),
    sa.Column('product_name', sa.String(length=255), nullable=True),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('typ', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('sell_price', sa.Float(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['quotation_id'], ['quotation.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quotation_item')
    op.drop_table('labor_paid')
    op.drop_table('bank_transaction')
    op.drop_table('supplier')
    op.drop_table('quotation')
    op.drop_table('project')
    op.drop_table('panel')
    op.drop_table('labor')
    op.drop_table('inverter')
    op.drop_table('frame')
    op.drop_table('expanse')
    op.drop_table('dc_cable')
    op.drop_table('customer')
    op.drop_table('battery')
    op.drop_table('banks')
    op.drop_table('accessories')
    op.drop_table('ac_cable')
    op.drop_table('user')
    # ### end Alembic commands ###
