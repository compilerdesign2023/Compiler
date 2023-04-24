let s=String "this is a string" in
let l=s.length in
let n=0 in
let i=1 in
{
    for i<l-1 up i+=1 do
        let next=i+1 in
        let c=s.slice i next 1 in
        let e=String " " in
        if c==e then {
            n=n+1;
        }; end;
    print n+1;
} end
