#include <QApplication>
#include <QQmlApplicationEngine>

#include "Box2D/Box2D.h"

#include <QQuickItem>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    app.setOrganizationName("SLAM_Qt");
    QQmlApplicationEngine appEngine(QUrl("qrc:/main.qml"));
    return app.exec();
}
