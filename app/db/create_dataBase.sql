CREATE DATABASE IF NOT EXISTS Futbol_Base;

USE Futbol_Base;

CREATE TABLE IF NOT EXISTS Jugadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    nivel_habilidad DECIMAL NOT NULL,
    apodo VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    NombreEquipo VARCHAR(100) NOT NULL,
    Logo VARCHAR(255),
    IDCreador INT NOT NULL,
    EquipoCompleto BOOLEAN NOT NULL,
    Promedio_Habilidad DECIMAL(5,2),  -- Promedio de habilidad como DECIMAL
    Promedio_Edad INT,                -- Promedio de edad como INT
    CantidadJugadores INT DEFAULT 0,
    FOREIGN KEY (IDCreador) REFERENCES Jugadores(id)
);

CREATE TABLE IF NOT EXISTS JugadoresEquipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    IDJugador INT NOT NULL,
    IDEquipo INT NOT NULL,
    Fecha_Ingreso DATETIME NOT NULL,
    EstadoSolicitud VARCHAR(50) NOT NULL,
    SolicitudCreadaPor ENUM('jugador', 'equipo') NOT NULL,  -- Campo añadido para definir quien hizo la solicitud
    UNIQUE (IDJugador, IDEquipo),
    FOREIGN KEY (IDJugador) REFERENCES Jugadores(id),
    FOREIGN KEY (IDEquipo) REFERENCES Equipos(id)
);

CREATE TABLE IF NOT EXISTS Partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Id_EquipoCreador INT NOT NULL,
    Id_EquipoRival INT NOT NULL,
    nombre_cancha VARCHAR(100) NOT NULL,
    dirección_cancha VARCHAR(255) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado_partido BOOLEAN NOT NULL,
    FOREIGN KEY (Id_EquipoCreador) REFERENCES Equipos(id),
    FOREIGN KEY (Id_EquipoRival) REFERENCES Equipos(id)
);

CREATE TABLE IF NOT EXISTS Reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Id_EquipoReportador INT NOT NULL,
    Id_EquipoReportado INT NOT NULL,
    Id_Partido INT NOT NULL,
    reporte TEXT NOT NULL,
    FOREIGN KEY (Id_EquipoReportador) REFERENCES Equipos(id),
    FOREIGN KEY (Id_EquipoReportado) REFERENCES Equipos(id),
    FOREIGN KEY (Id_Partido) REFERENCES Partidos(id)
);
