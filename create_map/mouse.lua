-- Mode:
--  normal: fillColor = white
--  add:    fillColor = green
--  move:   fillColor = blue
--  delete: fillColor = red
--  color:  fillColor = yellow



Mouse = Node:extend()

function Mouse:new()
    mouse_x, mouse_y = love.mouse.getPosition()
    Mouse.super.new(self, mouse_x, mouse_y)
    self.ori_radius = self.radius
    self.ori_fillColor = self.fillColor
    self.ori_fontSize = self.fontSize
    self.id = 0
    self.radius = 10
    self.fontSize = 5
    self.mode = "normal"
    self.isLink = false
    self.isDelLink = false
    self.linkSrc = 0
end

-------- Set Mode
function Mouse:set_mode_normal()
    self.mode = "normal"
    self.fillColor = node_color.white
    self.radius = 10
    self.fontSize = 5
end
function Mouse:set_mode_add()
    self.mode = "add"
    self.fillColor = self.ori_fillColor
    self.radius = self.ori_radius
    self.fontSize = self.ori_fontSize
end
function Mouse:set_mode_move()
    self.mode = "move"
    self.fillColor = node_color.blue
    self.radius = 10
    self.fontSize = 5
end
function Mouse:set_mode_delete()
    self.mode = "delete"
    self.fillColor = node_color.red
    self.radius = 10
    self.fontSize = 5
end
function Mouse:set_mode_color()
    self.mode = "color"
    self.fillColor = node_color.yellow
    self.radius = 10
    self.fontSize = 5
end
-------- Set Mode End

-------- Detect Mode
function Mouse:is_mode_normal()
    if self.mode == "normal" then
        return true
    else
        return false
    end
end
function Mouse:is_mode_add()
    if self.mode == "add" then
        return true
    else
        return false
    end
end
function Mouse:is_mode_move()
    if self.mode == "move" then
        return true
    else
        return false
    end
end
function Mouse:is_mode_delete()
    if self.mode == "delete" then
        return true
    else
        return false
    end
end
function Mouse:is_mode_color()
    if self.mode == "color" then
        return true
    else
        return false
    end
end
-------- Detect Mode End

function Mouse:is_link()
    return self.isLink
end

function Mouse:set_link()
    self.isLink = true
end

function Mouse:set_not_link()
    self.isLink = false
end

function Mouse:set_link_src(id)
    self.linkSrc = id
end

function Mouse:get_linkSrc_id()
    return self.linkSrc
end

function Mouse:is_del_link()
    return self.isDelLink
end

function Mouse:set_del_link()
    self.isDelLink = true
end

function Mouse:set_not_del_link()
    self.isDelLink = false
end

function Mouse:set_del_link_src(id)
    self.linkSrc = id
end

function Mouse:get_delLinkSrc_id()
    return self.linkSrc
end

function Mouse:hit_node_detect(posi_range)
    if self.x < posi_range.right_x and
        self.x > posi_range.left_x and
        self.y > posi_range.top_y and
        self.y < posi_range.bottom_y then
        return true
    else
        return false
    end
end

function Mouse:update(dt)
    self.x, self.y = love.mouse.getPosition()
end

function Mouse:draw()
    Mouse.super.draw(self)
end
