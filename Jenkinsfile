agentLabel = "FF"
pipeline{
    agent any
    parameters {
        // string(name: 'octane_test_result_name_run_regex_pattern',defaultValue: '\\(int\\)\\[\\d*\\]', description: '' )
        string(name: 'testsToRunConverted',description: '' )
    }

    stages {

        stage('Run Tests') {
            agent{
                label agentLabel
            }
            steps {
                convertTestsToRun format:'', framework: 'mvnSurefire'
                script {
                    bat 'call mvn clean test -fn -Dtest="%testsToRunConverted%" '
                    // bat 'call move "C:\\JenkinsAgent\\workspace\\RunTestsPip\\target\\surefire-reports\\*.xml" "C:\\JenkinsAgent\\workspace\\RunTestsPip\\"'
                    // bat 'call mvn clean test -fn'
                }
                catchError {
                    archiveArtifacts artifacts: 'target/surefire-reports/*.xml', onlyIfSuccessful: false
                    // archiveArtifacts artifacts: '*.xml', onlyIfSuccessful: false
                    publishMicroFocusTestResults 'ONLY_ARCHIVE_FAILED_TESTS_REPORT'
                    // junit allowEmptyResults: true, testResults: '*Test.xml'
                    junit allowEmptyResults: true, testResults: 'target/surefire-reports/*.xml'
                    publishMicroFocusTestResults 'DONT_ARCHIVE_TEST_REPORT'
                }

            }

        }

    }
    // post {
    //     always {
    //         // collectPullRequestsToAlmOctane configurationId: '7c8acf03-7e5e-45e5-bab6-5db89b102bf2', credentialsId: 'ce04e494-cc7c-4bb0-b42b-3aa56bfd7ea7', repositoryUrl: 'https://github.com/andreibangau99/junit-tests.git', scmTool: 'github_cloud', sourceBranchFilter: '', targetBranchFilter: '', workspaceId: '17004'
    //         node(agentLabel) {
    //           cleanWs()
    //         }
    //         cleanWs()
    //     }
    // }

}
