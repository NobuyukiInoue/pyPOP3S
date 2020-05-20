# pyPOP3S

POP3 and POP3 over SSL/TLS client by python3.

## Relation

* pyPOP3S on AWS Lambda<BR>
[http://www.asahi-net.or.jp/~gx3n-inue/apps/pypop3s/index.html](http://www.asahi-net.or.jp/~gx3n-inue/apps/pypop3s/index.html)


## Usage

```
$ python pyPOP3S.py <pop3 server> <110 | 995> [username] [password]
```

## Execution example
```
$ python pyPOP3S.py pop.example.com 995
username: username      <--- input username.
Password: ********      <--- input password. 
connected to xxxxxxx:xxx
+OK please send PASS command
+OK your maildrop has xxx message(s)
xxx mails, xxxxxx bytes.
   1: <Data>                                   <From>
      <Subject>
   2: <Date>                                   <From>
      <Subject>
   3: <Date>                                   <From>
      <Subject>
   ...
   ...

select[1-169](0...list, -1 ...exit) : 1   <--- print mail No.1
   ...
   ...

select[1-169](0...list, -1 ...exit) : 2   <--- print mail No.2
   ...
   ...

select[1-169](0...list, -1 ...exit) : -1   <--- quit
```

## Licence

[MIT](https://github.com/NobuyukiInoue/pyPOP3S/blob/master/LICENSE)


## Author

[Nobuyuki Inoue](https://github.com/NobuyukiInoue/)
