# apkpure_get

This is a super simple tool for yanking APK's to reverse engineer from the APKPure service.  
It is not well written and has a zillion bugs but it works.
It is designed to be ran from other scripts. For example... If you have a list of the top 100 apps on the app store like "com.whatever.blah", do this...

```
cat top_apps.txt | parallel -j 20 python apkpure_get.py
```

I am hoping to pipeline this with automatic decompilation and analysis sometime, probably by feeding the apps downloaded to MobiSF or Jeb2 or something? idk.
