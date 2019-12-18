node {
  stage('SCM') {
    checkout poll: false, scm: [$class: 'GitSCM', branches: [[name: 'dev']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://n002tbs0@ec.europa.eu/cefdigital/code/scm/ebsi/4-eidas-bridge.git', credentialsId: 'EBSI_Jara']]]
  }
  stage('SonarQube Analysis') {
        sh "/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/sonar-scanner/bin/sonar-scanner -Dsonar.host.url=https://infra.ebsi.xyz/sonar -Dsonar.projectName=4-eidas-bridge -Dsonar.projectVersion=1.0 -Dsonar.projectKey=4-eidas-bridge -Dsonar.sources=. -Dsonar.projectBaseDir=/var/lib/jenkins/workspace/4-eidas-bridge"
    }
  }