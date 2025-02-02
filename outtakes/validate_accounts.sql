with data as (
	select * from account_data
),

subaccount_sum as (
	select parent_account_id, sum(value) as sum_value
	from data
	where parent_account_id is not null
	group by 1
),

compare_data as (
	select
		parent.id as parent_id,
		parent.name as parent_name,
		parent.value as parent_value,
		children.sum_value as children_value
	from data parent
	left join subaccount_sum children
		on children.parent_account_id = parent.id
	where children.parent_account_id is not null
)

select * from compare_data
where parent_value <> children_value
