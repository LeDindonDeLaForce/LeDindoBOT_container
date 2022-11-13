-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 192.168.2.254
-- Généré le : mar. 08 nov. 2022 à 17:33
-- Version du serveur : 10.9.3-MariaDB-1:10.9.3+maria~ubu2204
-- Version de PHP : 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `TWITCH_BOT`
--

-- --------------------------------------------------------

--
-- Structure de la table `CHANNEL_LIST`
--

CREATE TABLE `CHANNEL_LIST` (
  `id` int(255) NOT NULL,
  `channel` varchar(25) NOT NULL,
  `queue` tinyint(1) NOT NULL DEFAULT 0,
  `roulette` varchar(7) NOT NULL DEFAULT 'stopped'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------

--
-- Structure de la table `commands`
--

CREATE TABLE `commands` (
  `command` varchar(40) NOT NULL,
  `channel` int(10) NOT NULL,
  `text` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



-- --------------------------------------------------------

--
-- Structure de la table `quoteauthors`
--

CREATE TABLE `quoteauthors` (
  `channel` int(10) NOT NULL,
  `allowedauthor` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



-- --------------------------------------------------------

--
-- Structure de la table `routines`
--

CREATE TABLE `routines` (
  `channel` int(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `seconds` int(11) NOT NULL,
  `minutes` int(11) NOT NULL,
  `hours` int(11) NOT NULL,
  `routine_text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `stream_queue`
--

CREATE TABLE `stream_queue` (
  `id` int(10) NOT NULL,
  `channel` int(10) NOT NULL,
  `user` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





--
-- Index pour la table `CHANNEL_LIST`
--
ALTER TABLE `CHANNEL_LIST`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `channel` (`channel`);

--
-- Index pour la table `commands`
--
ALTER TABLE `commands`
  ADD PRIMARY KEY (`command`,`channel`),
  ADD KEY `channel` (`channel`);

--
-- Index pour la table `quoteauthors`
--
ALTER TABLE `quoteauthors`
  ADD PRIMARY KEY (`channel`,`allowedauthor`);

--
-- Index pour la table `routines`
--
ALTER TABLE `routines`
  ADD PRIMARY KEY (`channel`);

--
-- Index pour la table `stream_queue`
--
ALTER TABLE `stream_queue`
  ADD PRIMARY KEY (`channel`,`user`),
  ADD UNIQUE KEY `id_2` (`id`),
  ADD KEY `channel` (`channel`),
  ADD KEY `id` (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `CHANNEL_LIST`
--
ALTER TABLE `CHANNEL_LIST`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1188;

--
-- AUTO_INCREMENT pour la table `stream_queue`
--
ALTER TABLE `stream_queue`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=277;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `commands`
--
ALTER TABLE `commands`
  ADD CONSTRAINT `commands_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `CHANNEL_LIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `quoteauthors`
--
ALTER TABLE `quoteauthors`
  ADD CONSTRAINT `quoteauthors_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `CHANNEL_LIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `routines`
--
ALTER TABLE `routines`
  ADD CONSTRAINT `routines_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `CHANNEL_LIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `stream_queue`
--
ALTER TABLE `stream_queue`
  ADD CONSTRAINT `stream_queue_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `CHANNEL_LIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
