# CDXGEN-test-scripts
Quickly creates a docker container and runs some scripts to manually test out cdxgen on multiple projects.

This repository will hold github links to many projects in different languages.

Todo:
1) run cdxgen container
2) do a git pull to a chosen branch (maybe a gh pull in the future)
3) run the desired project, with custom arguments
4) quickly compare the results using (custom-bom-diff)


```bash
python ./src/cli.py -g https://github.com/signalapp/Signal-Android.git -e "sdk install java 17.0.13-tem" -a "-t java --deep" -r "./gradlew compilePlayStagingInstrumentationAndroidTestJavaWithJavac"
```

```
# oh-my-zsh extension for git has useful aliases:
gl = "git pull"
gp = "git push"
gcsm = "git commit --signoff --message"
```