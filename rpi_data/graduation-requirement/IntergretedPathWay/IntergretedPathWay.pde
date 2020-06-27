void setup(){
  String[] lines = loadStrings("info.txt");
  for (int i = 0 ; i < lines.length; i++) {
    String[] list = split(lines[i], ' ');
     print(",\"" + list[0] + ' ' + list[1] + "\"");
  }
  print(".");
}