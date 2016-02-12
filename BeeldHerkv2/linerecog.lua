
local DEBUG = 2;
local BM = 1;
local bmTbl = {};

--[[
	Load in basic things
]]
if (BM >= 1) then
	bmTbl.setup = os.clock();
end;

-- Add the ./lua/ folder to the list of paths
package.path = "lua/?.lua;lualib/?.lua;"..package.path;

-- Load in the libs, store them as locals for fast access
local require = require;
local bitmap = require("bitmap");
local libjpeg = require("libjpeg");

-- Localize global libraries
local ipairs = ipairs;
local math = math;
local os = os;
local print = print;
local table = table;

-- Program vars
local width, height = 480, 256;
local getPixel, setPixel;

-- Generate a list of pixels to iterate over
local pixelList = {};
do
	local interval = 4;
	local distFromTop = 10;
	local distFromBottom = 20;
	for i = 1, (width / interval) - 1 do
		local x = i * interval;
		local y = math.floor((height - (distFromTop + distFromBottom)) * ((width - x * 2) / width) ^ 4);
		pixelList[#pixelList + 1] = {x, distFromTop + y};
	end;
end;

local function calcDiffs(getPixel)
	local previous = pixelList[1];
	local previousLuma = getPixel(previous[1], previous[2]);
	local lumaDiffList = {};
	for i, current in ipairs(pixelList) do
		local luma = getPixel(current[1], current[2]);
		local diff = previousLuma - luma;
		if (diff < -10 or diff > 10) then
			current[3] = diff;
			lumaDiffList[#lumaDiffList + 1] = math.abs(diff);
		end;

		previous = current;
		previousLuma = luma;
	end;

	table.sort(lumaDiffList);

	for i = 1, #lumaDiffList do
		if (lumaDiffList[i + 1] - lumaDiffList[i] > 2) then
			if (DEBUG >= 1) then
				print("Threshold:", lumaDiffList[i + 1]);
			end;
			return lumaDiffList[i + 1];
		end;
	end;

	return 0;
end;

local function getIntersectPoints(diffThreshold)
	local pointList = {};
	local inLine;
	for i, current in ipairs(pixelList) do
		if (current[3]) then
			if (current[3] < -diffThreshold and (not inLine or inLine + 3 < i)) then
				inLine = i;
				if (DEBUG >= 1) then
					if (DEBUG >= 2) then
						print("Line enter", i);
					end;
					setPixel(current[1], current[2], 128, 255, 255);
					setPixel(current[1] + 1, current[2], 128, 255, 255);
					setPixel(current[1] - 1, current[2], 128, 255, 255);
					setPixel(current[1], current[2] + 1, 128, 255, 255);
					setPixel(current[1], current[2] - 1, 128, 255, 255);
				end;
			elseif (current[3] > diffThreshold and inLine) then
				if (i - inLine < #pixelList / 10) then
					pointList[#pointList + 1] = {math.floor((pixelList[inLine][1] + current[1]) / 2), math.floor((pixelList[inLine][2] + current[2]) / 2)};
				end;
				inLine = false;
				if (DEBUG >= 1) then
					if (DEBUG >= 2) then
						print("Line exit", i);
					end;
					setPixel(current[1], current[2], 128, 0, 0);
					setPixel(current[1] + 1, current[2], 128, 0, 0);
					setPixel(current[1] - 1, current[2], 128, 0, 0);
					setPixel(current[1], current[2] + 1, 128, 0, 0);
					setPixel(current[1], current[2] - 1, 128, 0, 0);
				end;
			elseif (DEBUG >= 1) then
				setPixel(current[1], current[2], 128, 255, 0);
			end;
		elseif (DEBUG >= 1) then
			setPixel(current[1], current[2], 0, 128, 128);
		end;

		current[3] = false;
	end;

	return pointList;
end;

function getTargetPoint(imagePath)
	if (BM >= 1) then
		bmTbl.total = os.clock();
	end;

	--[[
		Load in the image and setup get/setPixel functions
	]]
	if (BM >= 1) then
		bmTbl.load = os.clock();
	end;

	local image = libjpeg.load({path = imagePath});
	local getPxl, setPxl = bitmap.pixel_interface(image);
	if (DEBUG >= 1) then
		getPixel, setPixel = getPxl, setPxl;
	end;

	if (bmTbl.load) then
		print("---- Load time:", os.clock() - bmTbl.load);
	end;

	--[[
		Get diff threshold
	]]
	if (BM >= 1) then
		bmTbl.threshold = os.clock();
	end;

	local diffThreshold = calcDiffs(getPxl);

	if (bmTbl.threshold) then
		print("---- Thres time:", os.clock() - bmTbl.threshold);
	end;

	--[[
		Find line points along pixelList
	]]
	if (BM >= 1) then
		bmTbl.points = os.clock();
	end;

	local pointList = getIntersectPoints(diffThreshold);

	if (bmTbl.points) then
		print("---- Points time:", os.clock() - bmTbl.points);
	end;

	if (bmTbl.total) then
		print("---- Total time:", os.clock() - bmTbl.total);
	end;

	if (DEBUG >= 1) then
		for k, point in ipairs(pointList) do
			print("Point:", point[1], point[2])
			setPixel(point[1], point[2], 128, 0, 255);
			setPixel(point[1] + 1, point[2], 128, 0, 255);
			setPixel(point[1] - 1, point[2], 128, 0, 255);
			setPixel(point[1], point[2] + 1, 128, 0, 255);
			setPixel(point[1], point[2] - 1, 128, 0, 255);
		end;
	end;

	if (DEBUG >= 1) then
		libjpeg.save({bitmap = image, path = "test.jpg"});
	end;
end;

if (bmTbl.setup) then
	print("---- Setup time:", os.clock() - bmTbl.setup);
end;


--[[
	TEST STUFF
]]
local amount = tonumber(arg[2]) or 1;
if (amount ~= 1) then
	DEBUG = 0;
	BM = 0;
end;

local bmStart = os.clock();
for i = 1, amount do
	getTargetPoint(arg[1]);
end;
print("-----------------------")
print("Amount of runs:", amount);
print("Average time:", (os.clock() - bmStart) / amount);