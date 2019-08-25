#include <QApplication>
#include <QQmlApplicationEngine>

#include "Box2D/Box2D.h"

#include <QQuickItem>
class Lidar : public QQuickItem {
    Lidar(QQuickItem *parent = nullptr) : QQuickItem(parent)
    {

    };
    ~Lidar() = default;

    Q_PROPERTY(QPoint m_center MEMBER m_center NOTIFY centerChanged)

private:
    QPoint m_center;
};

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine appEngine(QUrl("qrc:/main.qml"));
    return app.exec();
}
