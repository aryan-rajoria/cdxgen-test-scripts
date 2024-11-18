
        cd /home/cyclonedx/
        source ~/.bashrc

        sdk install java 17.0.13-tem

        git clone https://github.com/CycloneDX/cdxgen.git 
        cd cdxgen

        corepack enable pnpm 
        pnpm install
        
        cd ..

        git clone --filter=blob:none https://github.com/signalapp/Signal-Android.git  # Use --filter=blob:none for faster cloning
        cd $(basename https://github.com/signalapp/Signal-Android.git .git)  # cd into the cloned repo directory

        ./gradlew compilePlayStagingInstrumentationAndroidTestJavaWithJavac  # Run the command inside the repo

        cd ..  # cd back to the previous directory

        

        node cdxgen/bin/cdxgen.js -t java --deep ./$(basename https://github.com/signalapp/Signal-Android.git .git) # Run cdxgen with provided arguments
    