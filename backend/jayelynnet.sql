with

-- get the masters
master as (
    select workorder_base_id, part_id, Calc_Qty
    from requirement r 
    inner join part_site_view p -- I think this is the table with the masters
        on p.part_id = r.workorder_base_id -- join on the master part
        and p.engineering_mst = r.engineering_mst -- get only the active master
    where type = 'M' -- only masters
    and calc_qty > 0 -- only those with positive quantity
),

-- get current on-hand balances
parts as (
    select part_id, 
           sum(case when type = 'I' then qty else -qty end) as qty
    from inventory_trans
    group by part_id
),

combo as (
    select m.workorder_base_id, 
           m.part_id, 
           m.Calc_Qty, 
           COALESCE(p.qty, 0) as on_hand, -- make sure no nulls
           FLOOR(COALESCE(p.qty, 0) / m.Calc_Qty) as complete_sets -- floor division to get whole sets
    from master m 
    left join parts p on m.part_id = p.part_id
)

-- get the total buildable amount
select 
    workorder_base_id, 
    min(complete_sets) as complete_sets -- minimum determines the limiting factor
from combo
group by workorder_base_id;
