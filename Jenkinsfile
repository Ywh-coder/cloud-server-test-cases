pipeline {
    agent any

    tools {
        jdk 'JDK21'
        allure 'Allure'
    }

    stages {
        stage('拉取代码') {
            steps {
                echo '正在从 GitHub 拉取代码...'
                git branch: 'main', url: 'https://github.com/Ywh-coder/cloud-server-test-cases.git'
            }
        }

        stage('安装依赖') {
            steps {
                echo '正在创建虚拟环境并安装依赖...'
                dir('02-Mall-testing') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('执行接口自动化测试') {
            steps {
                echo '正在运行 Pytest...'
                withCredentials([string(credentialsId: 'MALL_DB_PASSWORD', variable: 'DB_PWD')]) {
                    dir('02-Mall-testing') {
                        sh '''
                            . venv/bin/activate
                            mkdir -p report/allure-results


                            cat <<EOF > common/config.yaml
active_env: "test"
env:
  test:
    base_url: "http://172.22.190.48:8080"
    timeout: 10
    db:
      host: "172.22.190.48"
      port: 3306
      user: "root"
      password: "${DB_PWD}"
      database: "mall"
EOF
                            pytest testcases/ --alluredir=./report/allure-results
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo '生成 Allure 测试报告...'
            dir('02-Mall-testing') {
                allure includeProperties: false, jdk: '', results: [[path: 'report/allure-results']]
            }
        }
    }
}
