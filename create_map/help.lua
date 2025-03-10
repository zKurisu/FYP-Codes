Help = Object:extend()

function Help:new()
    self.msg = [[
h: Toggle help window
c: Color mode, left click to print color
a: Add mode, left click to add new node
d: Delete mode, left click to delete node
n: Normal mode, left click to link node]]
    local window_width = love.graphics.getWidth()
    local window_height = love.graphics.getHeight()
    self.width = 800
    self.height = 300
    self.x = (window_width-self.width)/2
    self.y = (window_height-self.height)/2
    self.fontSize = 20
    self.isShow = false
end

function Help:toggle_show()
    if self.isShow == false then
        self.isShow = true
    else
        self.isShow = false
    end
end

function Help:update(dt)
end

function Help:draw()
    if self.isShow then
        love.graphics.setColor(0.5, 0.5, 0.5)
        love.graphics.rectangle("fill",
            self.x, self.y,
            self.width, self.height)
        love.graphics.setColor(1, 1, 1)
        love.graphics.printf(self.msg,
            love.graphics.newFont(self.fontSize),
            self.x, self.y,
            1000)
    end
end
