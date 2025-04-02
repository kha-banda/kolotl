-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-02-2025 a las 01:34:48
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
-- Estructura de tabla para la tabla `coordenadas_recolecta`
--

CREATE TABLE `coordenadas_recolecta` (
  `ID_coordenadas` int(11) NOT NULL,
  `lat` double DEFAULT NULL,
  `longitud` double DEFAULT NULL,
  `ALT` double DEFAULT NULL,
  `temperatura` double DEFAULT NULL,
  `humedad` double DEFAULT NULL,
  `ID_recolecta` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `coordenadas_recolecta`
--

INSERT INTO `coordenadas_recolecta` (`ID_coordenadas`, `lat`, `longitud`, `ALT`, `temperatura`, `humedad`, `ID_recolecta`) VALUES
(1, 18.134852158786313, -97.09727009838628, 0, NULL, NULL, 9),
(2, 18.161111, -97.198889, 0, NULL, NULL, 10),
(3, 18.161111, -97.198889, 0, NULL, NULL, 11),
(4, 18.161111, -97.198889, 0, NULL, NULL, 12),
(5, 18.161111, -97.198889, 0, NULL, NULL, 13),
(6, 18.161111, -97.198889, 0, NULL, NULL, 14),
(7, 18.149722, -97.164167, 0, NULL, NULL, 15),
(8, 18.149722, -97.164167, 0, NULL, NULL, 16),
(9, 18.149722, -97.164167, 0, NULL, NULL, 18),
(10, 18.134853, -97.09727078443173, 0, NULL, NULL, 20),
(11, 18.1324, -97.0713, 0, NULL, NULL, 21),
(12, 17.954722, -97.021389, 0, NULL, NULL, 22),
(13, 17.954722, -97.021389, 0, NULL, NULL, 23),
(14, 17.954722, -97.021389, 0, NULL, NULL, 24),
(15, 18.134851650986942, -97.09727040666783, 0, NULL, NULL, 25),
(16, 18.13485188422624, -97.09727002181125, 0, NULL, NULL, 28),
(23, 18.134855040483018, -97.09725858336328, 1384.922474259469, 6, 68, 42);

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

--
-- Volcado de datos para la tabla `habitat`
--

INSERT INTO `habitat` (`ID`, `nombre`, `caracteristicas`, `fecha_creacion`, `ultima_actualizacion`) VALUES
(1, 'Selva Baja Caducifolia', 'Bosque donde la mayoría de los árboles pierden sus hojas en época seca. Ubicada en la región de la Costa y Mixteca Baja.', '2024-10-25 10:20:07', '2024-10-25 10:20:07'),
(2, 'Selva Alta Perennifolia', 'Bosque húmedo con vegetación densa y árboles altos. Se encuentra en zonas montañosas de la Sierra Norte y Sierra Mazateca.', '2024-10-25 10:20:07', '2024-10-25 10:20:07'),
(3, 'Bosque de Niebla', 'Bosque siempre cubierto de neblina, manteniendo alta humedad. Ubicado en la Sierra Norte entre 1,200 y 2,500 msnm.', '2024-10-25 10:20:07', '2024-10-25 10:20:07'),
(4, 'Bosque de Pino-Encino', 'Bosque de pinos y encinos en climas templados y húmedos. Predomina en la Sierra Norte y Sierra Sur.', '2024-10-25 10:20:07', '2024-10-25 10:20:07'),
(5, 'Matorral Xerófilo', 'Hábitat árido con cactus y matorrales espinosos. Ubicado en los Valles Centrales y Mixteca.', '2024-10-25 10:20:07', '2024-10-25 10:20:07'),
(6, 'Manglares', 'Ecosistema costero de alta salinidad. Ubicado en la costa de Oaxaca, como la Laguna de Chacahua.', '2024-10-25 10:20:07', '2024-10-25 10:20:07'),
(7, 'Pastizales de Altura', 'Zonas de alta altitud con gramíneas y arbustos resistentes al frío, ubicadas en las partes altas de las sierras de Oaxaca.', '2024-10-25 10:20:07', '2024-10-25 10:20:07');

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

--
-- Volcado de datos para la tabla `locacion`
--

INSERT INTO `locacion` (`ID`, `cp`, `pais`, `estado`, `municipio`, `colonia`, `fecha_creacion`, `ultima_actualizacion`) VALUES
(3, 0, 'México', 'Oaxaca', 'Teotitlán de Flores Magón', 'Desconocido', '2024-10-24 12:41:18', '2024-10-24 12:41:18'),
(4, 0, 'México', 'Oaxaca', 'San Antonio Nanahuatipam', 'Desconocido', '2024-10-28 12:30:24', '2024-10-28 12:30:24'),
(5, 0, 'México', 'Oaxaca', 'Teotitlán de Flores Magón', 'Teotitlán de Flores Magón Centro', '2024-11-13 10:19:14', '2024-11-13 10:19:14'),
(6, 0, 'México', 'Oaxaca', 'Santa María Tecomavaca', 'Santa María Tecomavaca Centro', '2024-11-13 11:55:51', '2024-11-13 11:55:51');

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
  `notas` text DEFAULT NULL,
  `ID_usuario` int(11) DEFAULT NULL,
  `ID_locacion` int(11) DEFAULT NULL,
  `ID_habitat` int(11) DEFAULT NULL,
  `ID_scorpion` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `recolecta`
--

INSERT INTO `recolecta` (`ID`, `fecha_captura`, `adultomacho`, `adultohembra`, `juvenilmacho`, `juvenilhembra`, `subadultomacho`, `subadultohembra`, `notas`, `ID_usuario`, `ID_locacion`, `ID_habitat`, `ID_scorpion`, `fecha_creacion`, `ultima_actualizacion`) VALUES
(9, '2024-10-08', 1, 0, 0, 0, 0, 0, '', 1, 3, 1, 1, '2024-10-25 10:41:10', '2024-10-25 10:41:10'),
(10, '2024-10-28', 44, 1, 1, 0, 0, 0, '', 1, 4, 1, 3, '2024-10-28 12:30:25', '2024-10-28 12:30:25'),
(11, '2024-10-28', 8, 2, 2, 0, 0, 0, '', 1, 4, 1, 1, '2024-10-28 12:31:59', '2024-10-28 12:31:59'),
(12, '2024-10-28', 2, 1, 0, 1, 0, 0, '', 1, 4, 1, 5, '2024-10-28 12:34:35', '2024-10-28 12:34:35'),
(13, '2024-10-28', 1, 0, 0, 0, 0, 0, '', 1, 4, 1, 4, '2024-10-28 12:35:35', '2024-10-28 12:35:35'),
(14, '2024-10-28', 2, 1, 3, 0, 0, 0, '', 1, 4, 1, 2, '2024-10-28 12:37:55', '2024-10-28 12:37:55'),
(15, '2024-10-28', 23, 6, 0, 0, 0, 0, '', 1, 4, 1, 3, '2024-10-28 12:40:41', '2024-10-28 12:40:41'),
(16, '2024-10-28', 6, 4, 4, 0, 0, 0, '', 1, 4, 1, 1, '2024-10-28 12:41:39', '2024-10-28 12:41:39'),
(18, '2024-10-28', 1, 0, 0, 0, 0, 0, '', 1, 4, 1, 2, '2024-10-28 12:43:32', '2024-10-28 12:43:32'),
(20, '2024-11-12', 10, 2, 0, 1, 0, 2, '', 1, 3, 1, 3, '2024-11-12 09:35:02', '2024-11-12 09:35:02'),
(21, '2024-11-13', 4, 1, 5, 0, 0, 5, '', 1, 5, 3, 2, '2024-11-13 10:19:14', '2024-11-13 10:19:14'),
(22, '2024-11-13', 20, 4, 0, 0, 0, 0, '', 1, 6, 1, 3, '2024-11-13 11:55:51', '2024-11-13 11:55:51'),
(23, '2024-11-13', 1, 0, 0, 0, 0, 0, '', 1, 6, 1, 1, '2024-11-13 11:56:47', '2024-11-13 11:56:47'),
(24, '2024-11-13', 1, 0, 0, 0, 0, 0, '', 1, 6, 1, 4, '2024-11-13 11:58:04', '2024-11-13 11:58:04'),
(25, '2024-11-14', 1, 1, 0, 0, 0, 0, '', 1, 3, 1, 2, '2024-11-14 12:22:28', '2024-11-14 12:22:28'),
(28, '2024-11-14', 0, 2, 0, 0, 0, 0, '', 1, 3, 1, 2, '2024-11-14 12:31:17', '2024-11-14 12:31:17'),
(42, '2024-12-16', 0, 0, 10, 0, 0, 0, 'hola', 1, 3, 1, 1, '2024-12-17 09:10:43', '2024-12-17 09:10:43');

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
  `descripcion` text DEFAULT NULL,
  `ID_veneno` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `scorpions`
--

INSERT INTO `scorpions` (`ID`, `orden`, `familia`, `superfamilia`, `subfamilia`, `genero`, `subgenero`, `especie`, `descripcion`, `ID_veneno`, `fecha_creacion`, `ultima_actualizacion`) VALUES
(1, 'Scorpiones', 'Buthidae', '', '', 'Centruroides', '', 'baergi', NULL, NULL, '2024-10-21 09:53:12', NULL),
(2, 'Scorpiones', 'Vaejovidae', '', '', 'Mesomexovis', '', 'subcristatus', NULL, NULL, '2024-10-31 09:56:56', NULL),
(3, 'Scorpiones', 'Vaejovidae', '', '', 'Mesomexovis', '', 'sp (fasciatus)', NULL, NULL, '2024-10-31 09:56:56', NULL),
(4, 'Scorpiones', ' Desconocido', '', '', 'Hoffmannihadrurus', '', 'aztecus', NULL, NULL, '2024-10-31 09:56:56', NULL),
(5, 'Scorpiones', ' Desconocido', '', '', 'Vaejovis', '', 'Solegladi', NULL, NULL, '2024-10-31 09:56:56', NULL);

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

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`ID`, `nombre`, `apellido`, `correo`, `contrasena`, `rol`, `fecha_creacion`, `ultima_actualizacion`) VALUES
(1, 'admin1', 'admin', 'admin@unca.edu.mx', '1234', 'admin', '2024-10-10 11:25:38', '2024-10-16 10:36:48'),
(2, 'user1', 'user1', 'user@unca.edu.mx', '1234', 'user', '2024-10-10 11:28:35', NULL),
(11, 'dario', 'castillo', 'ad@unca.edu.mx', '1234', 'user', '2024-11-22 09:45:33', '2024-11-22 09:45:33');

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
-- Indices de la tabla `coordenadas_recolecta`
--
ALTER TABLE `coordenadas_recolecta`
  ADD PRIMARY KEY (`ID_coordenadas`),
  ADD KEY `ID_recolecta` (`ID_recolecta`);

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
-- AUTO_INCREMENT de la tabla `coordenadas_recolecta`
--
ALTER TABLE `coordenadas_recolecta`
  MODIFY `ID_coordenadas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `fotos`
--
ALTER TABLE `fotos`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `habitat`
--
ALTER TABLE `habitat`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `locacion`
--
ALTER TABLE `locacion`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `publicacion`
--
ALTER TABLE `publicacion`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recolecta`
--
ALTER TABLE `recolecta`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT de la tabla `scorpions`
--
ALTER TABLE `scorpions`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `veneno`
--
ALTER TABLE `veneno`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `coordenadas_recolecta`
--
ALTER TABLE `coordenadas_recolecta`
  ADD CONSTRAINT `coordenadas_recolecta_ibfk_1` FOREIGN KEY (`ID_recolecta`) REFERENCES `recolecta` (`ID`);

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
