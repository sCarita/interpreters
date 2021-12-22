program Main;
   var c : integer;

procedure Alpha(a : integer; b : integer);
var x : integer;

   procedure Beta(a : integer; b : integer);
   var x : integer;
   begin
      x := a * 10 + b * 2;
   end;

begin
   x := (a + b) * 2 + c;

   Beta(5, 10);      { procedure call }
end;

begin { Main }
   c := 10;
   Alpha(3 + 5, 7);  { procedure call }

end.  { Main }