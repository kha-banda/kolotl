-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-10-2024 a las 20:24:07
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `scorpions`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fotos`
--

CREATE TABLE `fotos` (
  `ID` int(11) NOT NULL,
  `ruta` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habitat`
--

CREATE TABLE `habitat` (
  `ID` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `caracteristicas` text DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `locacion`
--

CREATE TABLE `locacion` (
  `ID` int(11) NOT NULL,
  `cp` int(11) NOT NULL,
  `pais` varchar(200) NOT NULL,
  `estado` varchar(200) NOT NULL,
  `municipio` varchar(250) NOT NULL,
  `colonia` varchar(250) NOT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `publicacion`
--

CREATE TABLE `publicacion` (
  `ID` int(11) NOT NULL,
  `nombre` varchar(250) NOT NULL,
  `ruta` varchar(250) NOT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `publicacion_scorpion`
--

CREATE TABLE `publicacion_scorpion` (
  `ID_scorpion` int(11) NOT NULL,
  `ID_publicacion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recolecta`
--

CREATE TABLE `recolecta` (
  `ID` int(11) NOT NULL,
  `fecha_captura` date DEFAULT NULL,
  `adultomacho` int(11) DEFAULT NULL,
  `adultohembra` int(11) DEFAULT NULL,
  `juvenilmacho` int(11) DEFAULT NULL,
  `juvenilhembra` int(11) DEFAULT NULL,
  `subadultomacho` int(11) DEFAULT NULL,
  `subadultohembra` int(11) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `longitud` double DEFAULT NULL,
  `ALT` double DEFAULT NULL,
  `notas` text DEFAULT NULL,
  `ID_usuario` int(11) DEFAULT NULL,
  `ID_locacion` int(11) DEFAULT NULL,
  `ID_habitat` int(11) DEFAULT NULL,
  `ID_scorpion` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recolecta_fotos`
--

CREATE TABLE `recolecta_fotos` (
  `ID_recolecta` int(11) NOT NULL,
  `ID_foto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `scorpions`
--

CREATE TABLE `scorpions` (
  `ID` int(11) NOT NULL,
  `orden` varchar(100) NOT NULL,
  `familia` varchar(100) NOT NULL,
  `superfamilia` varchar(100) NOT NULL,
  `subfamilia` varchar(100) NOT NULL,
  `genero` varchar(100) NOT NULL,
  `subgenero` varchar(100) NOT NULL,
  `especie` varchar(100) NOT NULL,
  `ID_veneno` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `scorpion_fotos`
--

CREATE TABLE `scorpion_fotos` (
  `ID_foto` int(11) NOT NULL,
  `ID_scorpion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `ID` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contrasena` varchar(50) NOT NULL,
  `rol` varchar(50) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `veneno`
--

CREATE TABLE `veneno` (
  `ID` int(11) NOT NULL,
  `nombre` varchar(250) NOT NULL,
  `tipo` varchar(250) NOT NULL,
  `sintomas` varchar(250) NOT NULL,
  `usos` text NOT NULL,
  `formula` text NOT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `fotos`
--
ALTER TABLE `fotos`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `habitat`
--
ALTER TABLE `habitat`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `locacion`
--
ALTER TABLE `locacion`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `publicacion`
--
ALTER TABLE `publicacion`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `publicacion_scorpion`
--
ALTER TABLE `publicacion_scorpion`
  ADD PRIMARY KEY (`ID_scorpion`,`ID_publicacion`),
  ADD KEY `ID_publicacion` (`ID_publicacion`);

--
-- Indices de la tabla `recolecta`
--
ALTER TABLE `recolecta`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID_usuario` (`ID_usuario`),
  ADD KEY `ID_locacion` (`ID_locacion`),
  ADD KEY `ID_habitat` (`ID_habitat`),
  ADD KEY `ID_scorpion` (`ID_scorpion`);

--
-- Indices de la tabla `recolecta_fotos`
--
ALTER TABLE `recolecta_fotos`
  ADD PRIMARY KEY (`ID_recolecta`,`ID_foto`),
  ADD KEY `ID_foto` (`ID_foto`);

--
-- Indices de la tabla `scorpions`
--
ALTER TABLE `scorpions`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID_veneno` (`ID_veneno`);

--
-- Indices de la tabla `scorpion_fotos`
--
ALTER TABLE `scorpion_fotos`
  ADD PRIMARY KEY (`ID_foto`,`ID_scorpion`),
  ADD KEY `ID_scorpion` (`ID_scorpion`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `veneno`
--
ALTER TABLE `veneno`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `fotos`
--
ALTER TABLE `fotos`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `habitat`
--
ALTER TABLE `habitat`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `locacion`
--
ALTER TABLE `locacion`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `publicacion`
--
ALTER TABLE `publicacion`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recolecta`
--
ALTER TABLE `recolecta`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `scorpions`
--
ALTER TABLE `scorpions`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `veneno`
--
ALTER TABLE `veneno`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `publicacion_scorpion`
--
ALTER TABLE `publicacion_scorpion`
  ADD CONSTRAINT `publicacion_scorpion_ibfk_1` FOREIGN KEY (`ID_scorpion`) REFERENCES `scorpions` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `publicacion_scorpion_ibfk_2` FOREIGN KEY (`ID_publicacion`) REFERENCES `publicacion` (`ID`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `recolecta`
--
ALTER TABLE `recolecta`
  ADD CONSTRAINT `recolecta_ibfk_1` FOREIGN KEY (`ID_usuario`) REFERENCES `usuarios` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `recolecta_ibfk_2` FOREIGN KEY (`ID_locacion`) REFERENCES `locacion` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `recolecta_ibfk_3` FOREIGN KEY (`ID_habitat`) REFERENCES `habitat` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `recolecta_ibfk_4` FOREIGN KEY (`ID_scorpion`) REFERENCES `scorpions` (`ID`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `recolecta_fotos`
--
ALTER TABLE `recolecta_fotos`
  ADD CONSTRAINT `recolecta_fotos_ibfk_1` FOREIGN KEY (`ID_recolecta`) REFERENCES `recolecta` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `recolecta_fotos_ibfk_2` FOREIGN KEY (`ID_foto`) REFERENCES `fotos` (`ID`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `scorpions`
--
ALTER TABLE `scorpions`
  ADD CONSTRAINT `scorpions_ibfk_1` FOREIGN KEY (`ID_veneno`) REFERENCES `veneno` (`ID`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `scorpion_fotos`
--
ALTER TABLE `scorpion_fotos`
  ADD CONSTRAINT `scorpion_fotos_ibfk_1` FOREIGN KEY (`ID_foto`) REFERENCES `fotos` (`ID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `scorpion_fotos_ibfk_2` FOREIGN KEY (`ID_scorpion`) REFERENCES `scorpions` (`ID`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
