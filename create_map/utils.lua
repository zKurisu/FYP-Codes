function cal_node_id()
    if #deleted_nodes_id ~= 0 then
        return table.remove(deleted_nodes_id)
    else
        return #nodes + 1
    end
end

function get_node_by_id(id)
    for _, n in ipairs(nodes) do
        if n:get_id() == id then
            return n
        end
    end
end

function cal_id_x(id, fontSize, offset)
    local id = id
    local unit_width = fontSize * 2/3 -- when 0 < id < 10
    local unit_len = 1 -- when 0 M id < 10; unit_len = 2 when 10 < id < 100
    while id >= 10 do
        id = id / 10
        unit_len = unit_len + 1
    end
    return offset - (unit_width * unit_len)/2 + 1
end

function set_selected_color(id)
    color_pallate_selected = id
end

function get_x_color(id)
    for _, x_color in pairs(node_color) do
        if x_color.id == id then
            return x_color
        end
    end
end

function cal_color_pallate_x()
    color_num = 0
    for _, _ in pairs(node_color) do
        color_num = color_num + 1
    end
    pallate_len = color_num * color_pallate_gap
    window_width = love.graphics.getWidth()
    return (window_width-pallate_len)/2
end

function cal_color_pallate_y()
    return color_pallate_gap
end
