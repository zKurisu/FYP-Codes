-- FontSize: 20
--      height: 20
--      width: 20 * 2/3


Node = Object:extend()

node_color = {
    yellow = {red=1, green=1, blue=0, id=1},
    black  = {red=0, green=0, blue=0, id=2},
    white  = {red=1, green=1, blue=1, id=3},
    green  = {red=0, green=1, blue=0, id=4},
    blue   = {red=0, green=0, blue=1, id=5},
    gray   = {red=0.5, green=0.5, blue=0.5, id=6},
    red    = {red=1, green=0, blue=0, id=7},
}

function Node:new(id, x, y)
    self.id = id
    self.radius = 20
    self.x = x
    self.y = y
    self.fontSize = 10
    self.lineColor = node_color.black
    self.fillColor = node_color.white
    self.fontColor = node_color.black
    self.isMove = false
    self.isSelected = false
    self.isDelSelected = false
    self.links = {}
end

-- Just add position to links
function Node:link_to(n)
    local d_x = self.x - n.x
    local d_y = self.y - n.y
    local angle = math.atan2(math.abs(d_y), math.abs(d_x))
    local src_x = self.x + math.cos(angle) * n.radius
    local src_y = self.y + math.sin(angle) * n.radius
    local dst_x = n.x - math.cos(angle) * n.radius
    local dst_y = n.y - math.sin(angle) * n.radius
    if d_x > 0 and d_y > 0 then
        src_x = self.x - math.cos(angle) * n.radius
        src_y = self.y - math.sin(angle) * n.radius
        dst_x = n.x + math.cos(angle) * n.radius
        dst_y = n.y + math.sin(angle) * n.radius
    elseif d_x > 0 and d_y < 0 then
        src_x = self.x + math.cos(angle) * n.radius
        src_y = self.y - math.sin(angle) * n.radius
        dst_x = n.x + math.cos(angle) * n.radius
        dst_y = n.y - math.sin(angle) * n.radius
    elseif d_x < 0 and d_y > 0 then
        src_x = self.x + math.cos(angle) * n.radius
        src_y = self.y - math.sin(angle) * n.radius
        dst_x = n.x - math.cos(angle) * n.radius
        dst_y = n.y + math.sin(angle) * n.radius
    end
    if self:is_link_exist(n) == false then
        table.insert(self.links, {
            src_id = self.id,
            src_x = src_x,
            src_y = src_y,
            dst_id = n.id,
            dst_x = dst_x,
            dst_y = dst_y
        })
    end
end

function Node:del_link(n)
    for i, link in ipairs(self.links) do
        if link.dst_id == n:get_id() then
            table.remove(self.links, i)
            break
        end
    end
end

function Node:is_link_exist(n)
    for _, link in ipairs(self.links) do
        if link.dst_id == n:get_id() then
            return true
        end
    end
    return false
end

function Node:get_id()
    return self.id
end

function Node:toggle_move()
    if self.isMove == true then
        self.isMove = false
    else
        self.isMove = true
    end
end

function Node:set_fillColor(x_color)
    self.fillColor = x_color
end

function Node:is_move()
    return self.isMove
end

function Node:selected()
    self.isSelected = true
end

function Node:not_selected()
    self.isSelected = false
end

function Node:del_selected()
    self.isDelSelected = true
end

function Node:not_del_selected()
    self.isDelSelected = false
end

function Node:get_posi_range()
    return {
        left_x   = self.x - self.radius,
        right_x  = self.x + self.radius,
        top_y    = self.y - self.radius,
        bottom_y = self.y + self.radius
    }
end

function Node:update(dt)
    if self.isMove == true then
        self.x, self.y = love.mouse.getPosition()
    end

    for _, link in ipairs(self.links) do
        if link.dst_id == 0 then
            link.dst_x, link.dst_y = love.mouse.getPosition()
        end
    end

    if self.fillColor == node_color.black then
        self.fontColor = node_color.white
    else
        self.fontColor = node_color.black
    end
end

function Node:draw()
    -- Draw links
    for _, link in ipairs(self.links) do
        love.graphics.line(link.src_x, link.src_y, link.dst_x, link.dst_y)
    end

    -- fill circle
    love.graphics.setColor(self.fillColor.red, self.fillColor.green, self.fillColor.blue)
    love.graphics.circle("fill", self.x, self.y, self.radius)

    -- Draw id
    love.graphics.setColor(self.fontColor.red, self.fontColor.green, self.fontColor.blue)
    love.graphics.printf(self.id,
        love.graphics.newFont(self.fontSize),
        cal_id_x(self.id, self.fontSize, self.x),
        self.y-self.fontSize/2,
        100)

    -- Draw circle line  -- always black
    love.graphics.setColor(self.lineColor.red, self.lineColor.green, self.lineColor.blue)
    love.graphics.circle("line", self.x, self.y, self.radius)

    if self.isSelected then
        local x = self.x - 5
        local y = self.y + self.radius + 10
        love.graphics.circle("fill", x, y, 3)
    end
    if self.isDelSelected then
        local x = self.x + 5
        local y = self.y + self.radius + 10
        love.graphics.setColor(1, 0, 0)
        love.graphics.circle("fill", x, y, 3)
        love.graphics.setColor(1, 1, 1)
    end
end
