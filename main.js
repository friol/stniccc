/* stniccc and many other c's */

var globalFrameNum=0;

function lpadHex2digit(s)
{
	if (s.length==1)
	{
		return "0"+s;
	}
	
	return s;
}

function stPaletteToHTMLRGB(color,palette)
{
	var result="#ffffff";
	var curcolor=palette[(color)&0x0f];

	//Colors are stored as words in Atari-ST format 00000RRR0GGG0BBB
	
	var blu3=((curcolor&0x007))&0xff;
	var gre3=((curcolor&0x070)>>4)&0xff;
	var red3=((curcolor&0x700)>>8)&0xff;
	
	var realBlue=blu3<<5;
	var realGreen=gre3<<5;
	var realRed=red3<<5;

	var hexBlue = lpadHex2digit(realBlue.toString(16));
	var hexGreen = lpadHex2digit(realGreen.toString(16));
	var hexRed = lpadHex2digit(realRed.toString(16));

	result="#"+hexRed+hexGreen+hexBlue;

	return result;	
}

function updateScreen()
{
	var cvs=document.getElementById("mainCanvass");
	var ctx = document.getElementById("mainCanvass").getContext('2d');

	var isIndexedMode=stnicccFrameList[globalFrameNum][2];
	var needsToClearScreen=stnicccFrameList[globalFrameNum][0];

	if (needsToClearScreen==1)
	{
		ctx.fillStyle="#000000";
		ctx.fillRect(0,0,cvs.width,cvs.height);
	}
	
	if (isIndexedMode==1)
	{
		for (var p=0;p<stnicccFrameList[globalFrameNum][5][0].length;p++)
		{
			var curpol=stnicccFrameList[globalFrameNum][5][0][p];
			var col=curpol[0];
	
			var framePalette=stnicccFrameList[globalFrameNum][3];
			var curcolor=stPaletteToHTMLRGB(col,framePalette);
			
			ctx.fillStyle = curcolor;
			ctx.beginPath();
	
			for (var edge=0;edge<curpol[1].length;edge++)
			{
				var coordx=stnicccFrameList[globalFrameNum][4][curpol[1][edge]][0];
				var coordy=stnicccFrameList[globalFrameNum][4][curpol[1][edge]][1];
				
				if (edge==0) ctx.moveTo(coordx,coordy);
				else ctx.lineTo(coordx,coordy);
			}
	
			ctx.closePath();
			ctx.fill();		

			ctx.strokeStyle  = curcolor;
			ctx.lineWidth=0.50;
			ctx.beginPath();

			for (var edge=0;edge<curpol[1].length;edge++)
			{
				var coordx=stnicccFrameList[globalFrameNum][4][curpol[1][edge]][0];
				var coordy=stnicccFrameList[globalFrameNum][4][curpol[1][edge]][1];
				
				if (edge==0) ctx.moveTo(coordx,coordy);
				else ctx.lineTo(coordx,coordy);
			}

			ctx.closePath();
			ctx.stroke();
		}
	}
	else
	{
		for (var p=0;p<stnicccFrameList[globalFrameNum][5][0].length;p++)
		{
			var curpol=stnicccFrameList[globalFrameNum][5][0][p];
			var col=curpol[0];

			var framePalette=stnicccFrameList[globalFrameNum][3];
			var curcolor=stPaletteToHTMLRGB(col,framePalette);
			
			ctx.fillStyle = curcolor;
			ctx.beginPath();

			for (var edge=0;edge<curpol[1].length;edge++)
			{
				var coordx=curpol[1][edge][0];
				var coordy=curpol[1][edge][1];
				
				if (edge==0) ctx.moveTo(coordx,coordy);
				else ctx.lineTo(coordx,coordy);
			}
	
			ctx.closePath();
			ctx.fill();		
			ctx.stroke();

			//

			ctx.strokeStyle  = curcolor;
			ctx.lineWidth=0.50;
			ctx.beginPath();

			for (var edge=0;edge<curpol[1].length;edge++)
			{
				var coordx=curpol[1][edge][0];
				var coordy=curpol[1][edge][1];
				
				if (edge==0) ctx.moveTo(coordx,coordy);
				else ctx.lineTo(coordx,coordy);
			}

			ctx.closePath();
			ctx.stroke();
		}
	}

	var frameSpan=document.getElementById("frameCount");
	frameSpan.innerHTML="Frame "+globalFrameNum.toString();

	globalFrameNum+=1;
	if (globalFrameNum>=stnicccFrameList.length)
	{
		globalFrameNum=0;
	}
}

window.onload=function()
{
	var ctx = document.getElementById("mainCanvass").getContext('2d');

	//ctx.translate(0.9, 0.9);
	ctx.scale(2, 2);
	
	setInterval(updateScreen,50);
	//updateScreen();
}
