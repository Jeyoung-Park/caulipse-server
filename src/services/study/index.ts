import { Brackets, getRepository } from 'typeorm';
import { randomUUID } from 'crypto';
import Study from '../../entity/StudyEntity';
import {
  orderByEnum,
  paginationDTO,
  searchStudyDTO,
  studyDTO,
} from '../../types/study.dto';
import UserProfile from '../../entity/UserProfileEntity';
import { schedules } from '../../routes/study/study.controller';

const CATEGORY_COUNT = 7;

const countAllStudy = async ({
  categoryCodes,
  weekdayFilter,
  frequencyFilter,
  locationFilter,
}: paginationDTO) => {
  const query = await getRepository(Study).createQueryBuilder('study');

  if (categoryCodes && categoryCodes.length) {
    categoryCodes.forEach((code) => {
      if (code % 100 == 0) {
        // 상위 카테고리
        query.orWhere('study.categoryCode BETWEEN :from AND :to', {
          from: code,
          to: code + CATEGORY_COUNT,
        });
      } else {
        query.orWhere('study.categoryCode = :categoryCode', { code });
      }
    });
  }
  if (weekdayFilter && weekdayFilter.length) {
    weekdayFilter.forEach((weekday) => {
      query.orWhere('study.weekday like :weekday', { weekday: `%${weekday}%` });
    });
  }
  if (locationFilter && locationFilter.length) {
    locationFilter.forEach((location) => {
      query.orWhere('study.location like :location', {
        location: `%${location}%`,
      });
    });
  }
  if (frequencyFilter) {
    query.andWhere('study.frequency = :frequencyFilter', { frequencyFilter });
  }
  return await query.getCount();
};

const getAllStudy = async ({
  categoryCodes,
  weekdayFilter,
  frequencyFilter,
  locationFilter,
  hideCloseTag,
  orderBy,
  pageNo,
  limit,
}: paginationDTO) => {
  const sq = getRepository(Study)
    .createQueryBuilder('study')
    .leftJoinAndSelect('study.hostId', 'UserProfile');
  if (!hideCloseTag) {
    // off
    sq.addSelect('study.dueDate');
  }
  if (categoryCodes && categoryCodes.length) {
    categoryCodes.forEach((code) => {
      if (code % 100 == 0) {
        // 상위 카테고리
        sq.orWhere('study.categoryCode BETWEEN :from AND :to', {
          from: code,
          to: code + CATEGORY_COUNT,
        });
      } else {
        sq.orWhere('study.categoryCode = :categoryCode', { code });
      }
    });
  }
  if (weekdayFilter && weekdayFilter.length) {
    weekdayFilter.forEach((weekday) => {
      sq.orWhere('study.weekday like :weekday', { weekday: `%${weekday}%` });
    });
  }
  if (locationFilter && locationFilter.length) {
    locationFilter.forEach((location) => {
      sq.orWhere('study.location like :location', {
        location: `%${location}%`,
      });
    });
  }
  if (frequencyFilter) {
    sq.andWhere('study.frequency = :frequencyFilter', { frequencyFilter });
  }

  if (orderBy === orderByEnum.LATEST) {
    sq.orderBy('study.createdAt', 'DESC');
  } else if (orderBy === orderByEnum.LAST) {
    sq.orderBy('study.createdAt', 'ASC');
  } else if (orderBy === orderByEnum.SMALL_VACANCY) {
    sq.orderBy('study.vacancy', 'ASC');
  } else if (orderBy === orderByEnum.LARGE_VACANCY) {
    sq.orderBy('study.vacancy', 'DESC');
  } else if (orderBy === orderByEnum.FASTEST_DUEDATE) {
    sq.orderBy('study.dueDate', 'ASC');
  }
  return await sq
    .limit(limit)
    .offset((pageNo - 1) * limit)
    .getMany();
};

const getMyStudy = async (userId: string) => {
  return await getRepository(Study)
    .createQueryBuilder('study')
    .addSelect('study.dueDate')
    .leftJoinAndSelect('study.hostId', 'UserProfile')
    .where('study.HOST_ID = :userId', { userId })
    .orderBy('study.createdAt', 'ASC')
    .getMany();
};

const findStudyById = async (id: string) => {
  return await getRepository(Study)
    .createQueryBuilder('study')
    .addSelect('study.dueDate')
    .leftJoinAndSelect('study.hostId', 'UserProfile')
    .where('study.id = :id', { id })
    .getOne();
};

const updateStudyViews = async (study: Study) => {
  study.views += 1;
  return await getRepository(Study).save(study);
};

const createStudy = async (studyDTO: studyDTO, user: UserProfile) => {
  const {
    title,
    studyAbout,
    weekday,
    frequency,
    location,
    capacity,
    categoryCode,
    dueDate,
  } = studyDTO;
  const due = new Date(dueDate);
  const today = new Date();

  const studyId = randomUUID();
  const study = new Study();
  study.id = studyId;
  study.createdAt = today;
  study.title = title;
  study.studyAbout = studyAbout;
  study.weekday = weekday;
  study.frequency = frequency;
  study.location = location;
  study.capacity = capacity;
  study.membersCount = 0;
  study.vacancy = capacity;
  study.isOpen = true;
  study.hostId = user;
  study.views = 0;
  study.categoryCode = categoryCode;
  study.bookmarkCount = 0;
  study.dueDate = due;

  return await getRepository(Study).save(study);
};

const updateStudy = async (studyDTO: studyDTO, study: Study) => {
  const {
    title,
    studyAbout,
    weekday,
    frequency,
    location,
    capacity,
    categoryCode,
    dueDate,
  } = studyDTO;

  if (title) study.title = title;
  if (studyAbout) study.studyAbout = studyAbout;
  if (weekday) study.weekday = weekday;
  if (frequency) study.frequency = frequency;
  if (location) study.location = location;
  if (capacity) study.capacity = capacity;
  if (categoryCode) study.categoryCode = categoryCode;
  if (dueDate) {
    const due = new Date(dueDate);
    study.dueDate = due;
  }
  return await getRepository(Study).save(study);
};

const deleteStudy = async (study: Study) => {
  return await getRepository(Study).remove(study);
};

const searchStudy = async (searchStudyDTO: searchStudyDTO) => {
  const { keyword, weekdayFilter, frequencyFilter, locationFilter, orderBy } =
    searchStudyDTO;

  const query = getRepository(Study)
    .createQueryBuilder('study')
    .addSelect('study.dueDate')
    .leftJoinAndSelect('study.hostId', 'UserProfile')
    .where(
      new Brackets((qb) => {
        qb.where('study.title LIKE :keyword', {
          keyword: `%${keyword}%`,
        }).orWhere('study.studyAbout LIKE :keyword', {
          keyword: `%${keyword}%`,
        });
      })
    );

  if (weekdayFilter && weekdayFilter.length) {
    weekdayFilter.forEach((weekday) => {
      query.orWhere('study.weekday like :weekday', { weekday: `%${weekday}%` });
    });
  }
  if (locationFilter && locationFilter.length) {
    locationFilter.forEach((location) => {
      query.orWhere('study.location like :location', {
        location: `%${location}%`,
      });
    });
  }
  if (frequencyFilter) {
    query.andWhere('study.frequency = :frequencyFilter', { frequencyFilter });
  }

  if (orderBy === orderByEnum.LATEST) {
    query.orderBy('study.createdAt', 'DESC');
  } else if (orderBy === orderByEnum.LAST) {
    query.orderBy('study.createdAt', 'ASC');
  } else if (orderBy === orderByEnum.SMALL_VACANCY) {
    query.orderBy('study.vacancy', 'ASC');
  } else if (orderBy === orderByEnum.LARGE_VACANCY) {
    query.orderBy('study.vacancy', 'DESC');
  } else if (orderBy === orderByEnum.FASTEST_DUEDATE) {
    query.orderBy('study.dueDate', 'ASC');
  }
  return await query.getMany();
};

export const decreaseMemberCount = async (studyId: string) => {
  return getRepository(Study)
    .createQueryBuilder()
    .update()
    .set({
      membersCount: () => 'MEMBERS_COUNT - 1',
      vacancy: () => 'VACANCY + 1',
    })
    .where('ID = :id', { id: studyId })
    .execute();
};

export const increaseMemberCount = async (studyId: string) => {
  return getRepository(Study)
    .createQueryBuilder()
    .update()
    .set({
      membersCount: () => 'MEMBERS_COUNT + 1',
      vacancy: () => 'VACANCY - 1',
    })
    .where('ID = :id', { id: studyId })
    .execute();
};

export const closeStudy = async (study: Study) => {
  study.isOpen = false;
  if (process.env.NODE_ENV !== 'test') {
    schedules[`${study.id}`].cancel();
    delete schedules[`${study.id}`];
  }
  return await getRepository(Study).save(study);
};

export const findStudyByHostId = async (hostId: string) => {
  return getRepository(Study)
    .createQueryBuilder()
    .select()
    .where('HOST_ID = :id', { id: hostId })
    .execute();
};

export default {
  countAllStudy,
  getAllStudy,
  getMyStudy,
  findStudyById,
  updateStudyViews,
  createStudy,
  updateStudy,
  deleteStudy,
  searchStudy,
  decreaseMemberCount,
  increaseMemberCount,
  closeStudy,
  findStudyByHostId,
};
