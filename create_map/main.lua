#! /usr/bin/lua
--
-- main.lua
-- function
-- Copyright (Lua) Jie
-- 2025-02-22
--
--
love = require("love")

function love.load()
    love.graphics.setBackgroundColor(1, 1, 1)

    Object = require("classic")
    require("node")
    require("mouse")
    require("utils")
    require("help")

    nodes = {}
    deleted_nodes = {}
    deleted_nodes_id = {}

    color_pallate_radius = 20
    color_pallate_fontSize = 10
    color_pallate_selected = 1
    color_pallate_selected_gap = 10
    color_pallate_gap = 2*color_pallate_radius + 5
    color_pallate_x = cal_color_pallate_x()
    color_pallate_y = cal_color_pallate_y()

    -- debug_is_right = "False"
    -- debug_right_count = 0
    -- debug_links_num = 0
    -- debug_is_link = "False"

    m = Mouse()
    help = Help()
end

function love.mousepressed(x, y, button, istouch, presses)
    if button == 1 then
        if m:is_mode_add() then
            local new_id = cal_node_id()
            table.insert(nodes, Node(new_id, m.x, m.y))
        else
            for i, n in ipairs(nodes) do
                n_posi_range = n:get_posi_range()
                if m:hit_node_detect(n_posi_range) then
                    if m:is_mode_normal() then
                        if m:is_link() then
                            link_src = get_node_by_id(m:get_linkSrc_id())
                            link_src:del_link(m)
                            link_src:link_to(n)
                            link_src:not_selected()
                            m:set_not_link()
                            m:set_link_src(0)
                        else
                            n:link_to(m)
                            m:set_link_src(n:get_id())
                            m:set_link()
                            n:selected()
                        end
                    elseif m:is_mode_move() then
                        n:toggle_move()
                    elseif m:is_mode_delete() then
                        -- Delete node
                        table.remove(nodes, i)
                        table.insert(deleted_nodes, n)
                        table.insert(deleted_nodes_id, n:get_id())
                        for _, node in ipairs(nodes) do
                            node:del_link(n)
                        end
                    elseif m:is_mode_color() then
                        n:set_fillColor(get_x_color(color_pallate_selected))
                    end
                    break
                end
            end
        end
    end

    if button == 2 then
    --    debug_is_right = "True"
    --    debug_right_count = debug_right_count + 1
        if m:is_mode_add() then
        else
            for i, n in ipairs(nodes) do
                n_posi_range = n:get_posi_range()
                if m:hit_node_detect(n_posi_range) then
                    if m:is_mode_normal() then
                        -- Delete link
                        if m:is_del_link() then
                            link_src = get_node_by_id(m:get_delLinkSrc_id())
                            n:del_link(link_src)
                            link_src:del_link(n)
                            link_src:not_del_selected()
                            m:set_not_del_link()
                            m:set_del_link_src(0)
                        else
                            m:set_del_link_src(n:get_id())
                            m:set_del_link()
                            n:del_selected()
                        end
                    elseif m:is_mode_move() then
                    elseif m:is_mode_delete() then
                    end
                    break
                else
                    n:del_link(m)
                    n:not_selected()
                    n:not_del_selected()
                end
            end
        end
    end
end

function love.keypressed(key)
    if key == "n" then
        m:set_mode_normal()
    elseif key == "a" then
        m:set_mode_add()
    elseif key == "m" then
        m:set_mode_move()
    elseif key == "d" then
        m:set_mode_delete()
    elseif key == "c" then
        m:set_mode_color()
    elseif key == "h" then
        -- Toggle help msg
        help:toggle_show()
    elseif key == "1" then
        set_selected_color(1)
    elseif key == "2" then
        set_selected_color(2)
    elseif key == "3" then
        set_selected_color(3)
    elseif key == "4" then
        set_selected_color(4)
    elseif key == "5" then
        set_selected_color(5)
    elseif key == "6" then
        set_selected_color(6)
    elseif key == "7" then
        set_selected_color(7)
    end
end

function love.update(dt)
    for _, n in ipairs(nodes) do
        n:update()
    end
    m:update()
    help:update()

    if #nodes > 0 then
        debug_links_num = #nodes[1].links
    end

    if m:is_link() then
        debug_is_link = "True"
    else
        debug_is_link = "False"
    end
end

function love.draw()
    for _, n in ipairs(nodes) do
        n:draw()
    end
    m:draw()
    help:draw()

    -- Color list
    for _, x_color in pairs(node_color) do
        local x = color_pallate_x + x_color.id*color_pallate_gap
        local y = color_pallate_y
        love.graphics.setColor(0, 0, 0)
        love.graphics.circle("line", x, y, color_pallate_radius)
        love.graphics.setColor(x_color.red, x_color.green, x_color.blue)
        love.graphics.circle("fill", x, y, color_pallate_radius)
        love.graphics.setColor(0, 0, 0)
        love.graphics.printf(x_color.id,
            love.graphics.newFont(color_pallate_fontSize),
            cal_id_x(x_color.id, color_pallate_fontSize, x),
            y-color_pallate_fontSize/2,
            100)
        if x_color.id == color_pallate_selected then
            y = y + color_pallate_radius + color_pallate_selected_gap
            love.graphics.circle("fill", x, y, 3)
        end
    end

    -- love.graphics.print(#node_color * color_pallate_gap)
    -- Debug
    -- love.graphics.printf(m.x .. ", " .. m.y .. " " .. m.mode .. " nodesLen:" .. #nodes .. " delLen:" .. #deleted_nodes .. " isRight:" .. debug_is_right .. " count:" .. debug_right_count .. " linkNum:" .. debug_links_num .. " isLink:" .. debug_is_link,
    --     love.graphics.newFont(15),
    --     10, 10,
    --     100)
end
