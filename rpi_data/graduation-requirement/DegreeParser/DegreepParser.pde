void setup(){
  String raw = "or 4010* or 4070* or 4080* or 4140 or 4150 or 4240* or 4270 or 4440* or 4620* or 4640* or 4660* or 4670 or 4110 or 4200 or 4330* or 4340* or 4350* or 2120* or 2330* or 4710* or 4800*";
  String[] list = split(raw, ' ');
  String[] term = {"CIVL ", "ENEV ", "ERTH ", "MATH"};
  int[] sizes = {13, 5, 3, 1};
  int count = 0;
  for(int i = 0; i< list.length; i++)
  {
    if( list[i].equals("or"))
    {
      print( ", \"");
      if(sizes[count] == 0)
      {
        count++;
      }
      sizes[count]--;
      print(term[count]);
    }else
    {
      print(list[i] + "\"");
    }
  }
}