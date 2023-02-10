import anvil

def mcaCSV(csvFile,mcaPath):
    """
    Creates a CSV file from chunks of a newWorld of Minecraft.
    The algorithm traverse an area of chunks which size is ``chunkX``*``chunkZ`` chunks.
    Attributes
    ----------
    mcaPath: :class:`String`
        The .mca file path
    csvFile: :class:`File`
        An opened file to fill as CSV
    """
    region = anvil.Region.from_file(mcaPath)
    Bid = 0
    Cid = 0
    blockList = []
    head = "Bid;X;Y;Z;Tag;Cid;Cx;Cy\n"
    csvFile.write(head)
    for cx in range(0,2):
        for cz in range(0,2):
            chunk = anvil.Chunk.from_region(region, cx, cz)
            Cid = cx + cz 
            #get all blocks from chunck
            for x in range(0,15):
                for z in range(0,15):
                    for y in range(0,255):
                        Bid = x + y + z;
                        blockList.append([Bid,x,y,z,chunk.get_block(x,y,z).id,Cid,cx,cz])
            _makeCsv(csvFile,blockList)

def _makeCsv(file,blockList):
    for blockAtts in blockList:
        for i in range(0,len(blockAtts)):
            file.write(str(blockAtts[i]))
            if i < len(blockAtts)-1:
                file.write(";")
        file.write("\n")