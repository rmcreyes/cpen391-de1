-- Access point to connect to for sending HTTP requests
SSID = "REYES NETWORK"
SSID_PASSWORD = "********"

HOST = "backend391.herokuapp.com"

-- Meter ID of the associated parking meter
METER_ID = "603f24a1258f4a001c5a91ca"

-- Debug flag for debug printing
DEBUG = false


-- Configure ESP as a station
wifi.setmode(wifi.STATION)
wifi.sta.config(SSID,SSID_PASSWORD)
wifi.sta.autoconnect(1)

-- Pause for connection to take place
tmr.delay(1000000) -- wait 1,000,000 us = 1 second

-- This should print 5 if connection was successful
print(wifi.sta.status())

-- Prints the IP given to ESP8266
print(wifi.sta.getip())

-- Given an endpoint and a table representing the request's body, build a put request
function build_put_request(endpoint, body_table)
    body = "{"

    for param,value in pairs(body_table) do
        if (body ~= "{") then
            body = body .. ","
        end
        body = body .. "\n\""..param.."\": "..value
    end

    body = body .. "\n}"

    request = "PUT "..endpoint.." HTTP/1.1\r\n"..
    "Host: "..HOST.."\r\n"..
    "Connection: close\r\n"..
    "Content-Type: application/json\r\n"..
    "Content-Length: "..string.len(body).."\r\n"..
    "\r\n"..
    body

    if DEBUG then
        print(request)
    end

    return request
end

-- A callback function that prints the response of an HTTP request when received
function display_response(sck, response)
    print("Response:")
    print(response)
end

-- Given a request, send the request and have the response displayed when it is received
function send_http_request(request)
    ip = wifi.sta.getip()
    if (ip == nil) then
        print("Failed to connect, try again")
    else
        tmr.stop(0)
        if DEBUG then
            print("Connected to AP!")
            print(ip)
        end

        socket = net.createConnection(net.TCP, 0)
        socket:on("receive", display_response)
        socket:connect(80, HOST)

        socket:on("connection", function(sck)
            sck:send(request)
        end)
    end
end

-- Send a get request to the "/hello" endpoint
function hello_world()
    request = build_get_request("/hello")
    send_http_request(request)
end

-- Send a put request that notifies the server that a particular license plate has occupied the parking spot
function notify_license_plate_occupied(license_plate)
    body_table = {
        licensePlate = "\""..license_plate.."\"",
        isOccupied = "true"
    }

    endpoint = "/api/meter/"..METER_ID

    request = build_put_request(endpoint, body_table)
    send_http_request(request)
end

-- Send a put request that notifies the server that a particular license plate has left the parking spot
function notify_license_plate_left(license_plate)
    body_table = {
        licensePlate = "\""..license_plate.."\"",
        isOccupied = "false"
    }

    endpoint = "/api/meter/"..METER_ID

    request = build_put_request(endpoint, body_table)
    send_http_request(request)
end

-- Send a put request that confirms that the license plate we started the session with was correct
function confirm_parking_correct_license_plate(parking_id, license_plate)
    body_table = {
        isNew = "false",
        licensePlate = "\""..license_plate.."\""
    }

    endpoint = "/api/parking/confirm/"..parking_id

    request = build_put_request(endpoint, body_table)
    send_http_request(request)
end

-- Send a put request that corrects the license plate we started the session with
function confirm_parking_incorrect_license_plate(parking_id, license_plate)
    body_table = {
        isNew = "true",
        licensePlate = "\""..license_plate.."\""
    }

    endpoint = "/api/parking/confirm/"..parking_id

    request = build_put_request(endpoint, body_table)
    send_http_request(request)
end
