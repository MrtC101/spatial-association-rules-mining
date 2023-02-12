import anvil
import math

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
    blockList = []
    head = "Bid;X;Y;Z;Tag;ChunkX;ChunkZ\n"
    csvFile.write(head)
    for cx in range(0,2):
        for cz in range(0,9):
            chunk = anvil.Chunk.from_region(region, cx, cz)
            #get all blocks from chunck
            for x in range(0,15):
                for z in range(0,15):
                    for y in range(0,255):
                        Bid = x + y + z;
                        blockList.append([Bid,x,y,z,chunk.get_block(x,y,z).id,cx,cz])
            _makeCsv(csvFile,blockList)

def _makeCsv(file,blockList):
    for blockAtts in blockList:
        for i in range(0,len(blockAtts)):
            file.write(str(blockAtts[i]))
            if i < len(blockAtts)-1:
                file.write(";")
        file.write("\n")
"""
region = anvil.Region.from_file(".\\Data\\region_old\\r.0.0.mca")
chunk = anvil.Chunk.from_region(region, 0, 0)
block = chunk.get_block(10,40,10)
print(block.id)
region = anvil.Region.from_file(".\\Data\\region_new\\r.0.0.mca")
chunk = anvil.Chunk.from_region(region, 0, 0)
block = chunk.get_block(10,40,10)
print(block.id)
"""

