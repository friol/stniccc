
# 
# stniccc file parser
# (whatever stniccc means)
#

class stnicccFrame:

	def __init__(self):
		self.needsToClearScreen=False;
		self.containsPaletteData=False;
		self.isInIndexedMode=False;
		self.vertexList=[];
		self.polygonList=[];

	def updatePalette(self,paletteMask,thef,globalPalette):
		
		for x in range(0,16):
			if paletteMask&(1<<(15-x)):
				#print("Updating palette color ",15-x);
				thew=thef.read(2);
				color=int.from_bytes(thew,"big");
				globalPalette[x]=color;

	def readVertexData(self,thef,numVertex):
		
		for x in range(0,numVertex):
		
			byt=thef.read(1);
			posx=int.from_bytes(byt,"big");
			byt=thef.read(1);
			posy=int.from_bytes(byt,"big");

			self.vertexList.append([posx,posy]);		

	def readPolygon(self,thef,polyDesc):
		
		polyColor=(polyDesc>>4)&0x0f;
		vtxCount=polyDesc&0x0f;

		vtxList=[];
				
		for v in range(0,vtxCount):
			byt=thef.read(1);
			vtxIdx=int.from_bytes(byt,"big");
			vtxList.append(vtxIdx);	
			
		self.polygonList.append([polyColor,vtxList]);

	def readNonIndexedPolygon(self,thef,polyDesc):

		polyColor=polyDesc>>4;
		vtxCount=polyDesc&0x0f;

		vtxList=[];
		
		for v in range(0,vtxCount):
			byt=thef.read(1);
			posx=int.from_bytes(byt,"big");
			byt=thef.read(1);
			posy=int.from_bytes(byt,"big");
			
			vtxList.append([posx,posy]);
			
			self.polygonList.append([polyColor,vtxList]);

	def writeHeader(self,outf,frameNum):
		outf.write("var stnicccFrameList=[\n");

	def writeTrailer(self,outf,frameNum):
		outf.write("\n];\n");		
	
	def writeFrame(self,outf,frameNum,globalPalette):

		outf.write("//fn"+str(frameNum)+"\n");
		outf.write("[\n");
		
		if self.needsToClearScreen:
			outf.write("\t1,");
		else:
			outf.write("\t0,");

		if self.containsPaletteData:
			outf.write("1,");
		else:
			outf.write("0,");
			
		if self.isInIndexedMode:
			outf.write("1,\n");
		else:
			outf.write("0,\n");

		# palette data
		outf.write("\t[");
		for p in range(0,16):
			outf.write(str(globalPalette[p]));
			if p!=15:
				outf.write(",");
		outf.write("],\n");

		# vertices
		outf.write("\t");
		strVertexList=str(self.vertexList).replace(" ","");
		outf.write(strVertexList);
		outf.write(",\n");

		# polygons
		outf.write("\t[");
		strPolygonList=str(self.polygonList).replace(" ","");
		outf.write(strPolygonList);
		outf.write("]");

		# eoframe
		outf.write("\n],\n");		
	
	def readFrame(self,thef,globalPalette,frameNum):

		print("Processing frame ["+str(frameNum)+"]");
		
		byt=thef.read(1);
		frameOptions=int.from_bytes(byt,"big");
		if frameOptions&0x01:
			self.needsToClearScreen=True;
		if frameOptions&0x02:
			self.containsPaletteData=True;
		if frameOptions&0x04:
			self.isInIndexedMode=True;

		if self.containsPaletteData:
			
			wrd=thef.read(2);				
			paletteMask=int.from_bytes(wrd,"big");
			print("Palette mask is",hex(paletteMask));
			
			self.updatePalette(paletteMask,thef,globalPalette);
			
		if self.isInIndexedMode:
			
			byt=thef.read(1);
			numVertex=int.from_bytes(byt,"big");
			#print("There are ",numVertex," vertices in this frame. Reading them");
			
			self.readVertexData(thef,numVertex);
			
			endOfFrame=False;
			while not endOfFrame:
			
				byt=thef.read(1);
				polyDesc=int.from_bytes(byt,"big");
				#print("Poly descriptor: ",hex(polyDesc));
				
				if (polyDesc!=0xff) and (polyDesc!=0xfe) and (polyDesc!=0xfd):
					self.readPolygon(thef,polyDesc);
				else:
					if polyDesc==0xff:
						endOfFrame=True;
						return 0;
					elif polyDesc==0xfe:
						endOfFrame=True;
						return 0xfe;
					elif polyDesc==0xfd:
						endOfFrame=True;
						return 0xfd;
		else:
			
			endOfFrame=False;
			while not endOfFrame:

				byt=thef.read(1);
				polyDesc=int.from_bytes(byt,"big");
				#print("Poly descriptor: ",hex(polyDesc));

				if (polyDesc!=0xff) and (polyDesc!=0xfe) and (polyDesc!=0xfd):
					self.readNonIndexedPolygon(thef,polyDesc);
				else:
					if polyDesc==0xff:
						endOfFrame=True;
						return 0;
					elif polyDesc==0xfe:
						endOfFrame=True;
						return 0xfe;
					elif polyDesc==0xfd:
						endOfFrame=True;
						return 0xfd;
				
			
		return 0;
	
#

	
#
#
#

globalPalette=[0]*16;
frameNum=0;
fileBoundaryIndex=1;

dataFile = open("scene1.bin", "rb");
outFile = open("parsed.js","w");

newFrame=stnicccFrame();
newFrame.writeHeader(outFile,frameNum);

endOfFrames=False;
while not endOfFrames:
	retCode=newFrame.readFrame(dataFile,globalPalette,frameNum);
	newFrame.writeFrame(outFile,frameNum,globalPalette);
	frameNum+=1;
	newFrame=stnicccFrame();

	if retCode==0xfe:
		dataFile.seek(fileBoundaryIndex*65536);
		fileBoundaryIndex+=1;
	elif retCode==0xfd:
		endOfFrames=True;

	#if frameNum==1:
	#	endOfFrames=True;

newFrame.writeTrailer(outFile,frameNum);

outFile.close();
dataFile.close();
