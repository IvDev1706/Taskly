from sqlalchemy import Table, Column, MetaData, String, Integer, ForeignKey, DATE

#objeto de meta data
metadata = MetaData()

#tablas de la bd
prioprities = Table(
                "Priorities",
                metadata, 
                Column("id",Integer,autoincrement=True,primary_key=True),
                Column("name",String,nullable=False,unique=True)
            )

status = Table(
            "Status",
            metadata,
            Column("id",Integer,autoincrement=True,primary_key=True),
            Column("name",String,nullable=False,unique=True)
        )

task = Table(
        "Task",
        metadata,
        Column("id",String(5),primary_key=True),
        Column("desc",String,default="Sin descripcion"),
        Column("priority",Integer,ForeignKey("Priorities.id", ondelete="cascade"),nullable=False),
        Column("status",Integer,ForeignKey("Status.id", ondelete="cascade"),nullable=False,)
    )

project = Table(
            "Project",
            metadata,
            Column("id",String(5),primary_key=True),
            Column("name",String(30),default="Sin nombre"),
            Column("desc",String,default="Sin descripcion"),
            Column("delivery",DATE,nullable=False),
            Column("status",Integer,ForeignKey("Priorities.id", ondelete="cascade"), nullable=False),
        )

simpletask = Table(
                "SimpleTask",
                metadata,
                Column("id",String(5),ForeignKey("Task.id",ondelete="cascade"),primary_key=True),
                Column("title",String(20),default="Sin nombre"),
                Column("delivery",DATE,nullable=False)
            )

activity = Table(
            "Activity",
            metadata,
            Column("id",String(5),ForeignKey("Task.id", ondelete="cascade"),primary_key=True),
            Column("project",String(5),ForeignKey("Project.id", ondelete="cascade"),nullable=False)
        )